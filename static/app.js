const $ = (id) => document.getElementById(id);
let allRuns = [], data = null, step = 0, timer = null;

function parseValues(s) {
  if (!s.trim()) return [];
  const parts = s.trim().split(/[\s,;]+/);
  if (parts.some(x => !/^[-+]?\d+$/.test(x))) {
    throw Error('Chỉ được nhập số nguyên, phân cách bằng dấu phẩy, khoảng trắng hoặc chấm phẩy.');
  }
  const values = parts.map(Number);
  if (values.some(x => !Number.isSafeInteger(x))) {
    throw Error('Số nguyên nằm ngoài phạm vi an toàn của JavaScript.');
  }
  return values;
}

function stop() {
  clearInterval(timer);
  timer = null;
  $('play').textContent = '▶ Phát';
}

async function run() {
  stop();
  $('error').hidden = true;
  try {
    const values = parseValues($('values').value);
    const targets = parseValues($('target').value);
    if (targets.length < 1 || targets.length > 20) {
      throw Error('Hãy nhập từ 1 đến 20 khóa cần xóa.');
    }
    const response = await fetch('/api/analyze-batch', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({values, targets})
    });
    const body = await response.json();
    if (!response.ok) throw Error(body.error || 'Không thể xử lý yêu cầu.');
    allRuns = body.runs;
    const select = $('operationSelect');
    select.replaceChildren();
    for (let i = 0; i < allRuns.length; i++) {
      const item = document.createElement('option');
      item.value = String(i);
      item.textContent = `Lần ${i + 1}: Xóa ${allRuns[i].target}`;
      select.appendChild(item);
    }
    showOperation(0);
  } catch (error) {
    $('error').textContent = error.message;
    $('error').hidden = false;
  }
}

function showOperation(index) {
  if (!allRuns.length) return;
  stop();
  data = allRuns[index];
  $('operationSelect').value = String(index);
  $('operationInfo').textContent = `Đang xem lần ${index + 1}/${allRuns.length}. Dữ liệu đầu vào là cây sau lần xóa trước.`;
  step = 0;
  $('seek').max = data.frames.length - 1;
  render();
}

function draw(root, active, successor) {
  const svg = $('treeSvg');
  svg.replaceChildren();
  $('emptyTree').hidden = !!root;
  if (!root) {
    svg.setAttribute('viewBox', '0 0 800 330');
    svg.style.width = '800px';
    svg.style.height = '330px';
    return;
  }
  let index = 0;
  let count = 0;
  let maxDepth = 0;
  function layout(node, depth) {
    if (!node) return null;
    const left = layout(node.left, depth + 1);
    const x = 50 + index++ * 66;
    const y = 55 + depth * 90;
    const right = layout(node.right, depth + 1);
    count++;
    maxDepth = Math.max(maxDepth, depth);
    return {x, y, key: node.key, left, right};
  }
  const tree = layout(root, 0);
  const width = Math.max(700, count * 66 + 80);
  const height = Math.max(330, (maxDepth + 1) * 92 + 50);
  svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
  svg.style.width = width + 'px';
  svg.style.height = height + 'px';
  const ns = 'http://www.w3.org/2000/svg';
  function el(tag, attrs) {
    const obj = document.createElementNS(ns, tag);
    for (const [key, value] of Object.entries(attrs)) obj.setAttribute(key, value);
    return obj;
  }
  function paint(node) {
    if (!node) return;
    for (const child of [node.left, node.right]) {
      if (child) {
        svg.appendChild(el('line', {x1: node.x, y1: node.y, x2: child.x, y2: child.y}));
        paint(child);
      }
    }
    const cls = node.key === successor ? 'successor-node' :
                node.key === active ? 'active-node' : '';
    svg.appendChild(el('circle', {cx: node.x, cy: node.y, r: 23, class: cls}));
    const label = el('text', {x: node.x, y: node.y + 5, 'text-anchor': 'middle', 'font-size': '14'});
    label.textContent = node.key;
    svg.appendChild(label);
  }
  paint(tree);
}

function render() {
  if (!data) return;
  const frame = data.frames[step], after = data.after, stats = data.stats;
  draw(frame.tree, frame.active, frame.successor);
  $('stepInfo').textContent = frame.message;
  $('explain').textContent = frame.message;
  $('stepNum').textContent = `${step + 1} / ${data.frames.length}`;
  $('seek').value = step;
  $('rootStat').textContent = after.root ?? '∅';
  $('countStat').textContent = after.count;
  $('heightStat').textContent = after.height;
  // Moi frame co snapshot bo dem khi callback tu src/bst.py duoc kich hoat.
  // Chi dung bo dem cua FRAME dang xem, khong hien tong cuoi ngay tu buoc 1.
  const current = frame.progress || {
    search_nodes: stats.search_nodes ?? stats.comparisons,
    successor_visits: stats.successor_visits ?? 0,
    successor_steps: stats.successor_steps,
    cleanup_visits: stats.cleanup_visits ?? 0,
    total_visits: stats.total_visits ?? stats.comparisons
  };
  $('compareStat').textContent = current.search_nodes;
  $('searchProgress').textContent = current.search_nodes;
  $('successorVisitProgress').textContent = current.successor_visits;
  $('successorLeftProgress').textContent = current.successor_steps;
  $('cleanupProgress').textContent = current.cleanup_visits;
  $('costTotal').textContent = current.total_visits;
  $('costStage').textContent = `BƯỚC ${step + 1}/${data.frames.length}`;
  $('costExplanation').textContent = stats.case === 'hai_con'
    ? `Kế vị: ${stats.successor}; 1 nút đầu + ${stats.successor_steps} bước trái.`
    : stats.case === 'khong_tim_thay'
      ? 'Không tìm thấy khóa, không có thao tác kế vị.'
      : 'Xóa lá hoặc một con nên không tìm kế vị.';
  for (const [id, key] of [
    ['barSearch','search_nodes'], ['barSuccessor','successor_visits'],
    ['barLeft','successor_steps'], ['barCleanup','cleanup_visits']
  ]) {
    const maximum = Math.max(1, stats.search_nodes ?? stats.comparisons,
      stats.successor_visits ?? 0, stats.successor_steps, stats.cleanup_visits ?? 0);
    $(id).style.width = `${(100 * current[key] / maximum).toFixed(1)}%`;
  }
  $('successorStat').textContent = stats.successor ?? 'Không có';
  $('successorSteps').textContent = stats.successor_steps;
  $('validStat').textContent = after.valid ? '✓ Hợp lệ' : '✕ Không hợp lệ';
  $('beforeInorder').textContent = JSON.stringify(data.before.inorder);
  $('afterInorder').textContent = JSON.stringify(after.inorder);
  $('caseBadge').textContent = ({
    la:'NÚT LÁ', mot_con:'MỘT CON', hai_con:'HAI CON',
    khong_tim_thay:'KHÔNG TÌM THẤY'
  })[stats.case] || stats.case;
}

function go(index) {
  if (!data) return;
  step = Math.max(0, Math.min(index, data.frames.length - 1));
  render();
  if (step === data.frames.length - 1) stop();
}

$('run').onclick = run;
$('operationSelect').onchange = (event) => showOperation(Number(event.target.value));
$('prev').onclick = () => { stop(); go(step - 1); };
$('next').onclick = () => { stop(); go(step + 1); };
$('seek').oninput = (event) => { stop(); go(Number(event.target.value)); };
$('play').onclick = () => {
  if (!data) return;
  if (timer) { stop(); return; }
  if (step >= data.frames.length - 1) go(0);
  $('play').textContent = 'Ⅱ Tạm dừng';
  timer = setInterval(() => go(step + 1), Number($('speed').value));
};
$('speed').onchange = () => {
  if (timer) { stop(); $('play').click(); }
};
document.querySelectorAll('[data-values]').forEach(button => {
  button.onclick = () => {
    $('values').value = button.dataset.values;
    $('target').value = button.dataset.target;
    run();
  };
});
$('copy').onclick = async () => {
  if (!data) return;
  const text = allRuns.map((run, i) => (
    `Lần ${i + 1}: Xóa ${run.target}\n` +
    `Trước: ${JSON.stringify(run.before.inorder)}\n` +
    `Sau: ${JSON.stringify(run.after.inorder)}\n` +
    `Gốc: ${run.after.root ?? 'rỗng'}\n` +
    `Trường hợp: ${run.stats.case}\n` +
    `Kế vị: ${run.stats.successor ?? 'không có'}\n` +
    `Nút xét khi tìm khóa: ${run.stats.search_nodes}\n` +
    `Nút xét khi tìm kế vị: ${run.stats.successor_visits}\n` +
    `Bước đi trái: ${run.stats.successor_steps}\n` +
    `Nút xét khi xóa bản sao: ${run.stats.cleanup_visits}\n` +
    `Tổng lượt xét nút trong các pha: ${run.stats.total_visits}\n`
  )).join('\n');
  try {
    await navigator.clipboard.writeText(text);
    $('copy').textContent = '✓ Đã sao chép';
  } catch (error) {
    $('copy').textContent = 'Không thể sao chép';
  }
};
run();
