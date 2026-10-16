// Test simulation behavior without browser or npm dependencies.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const html = fs.readFileSync(path.join(__dirname, '../interactive/rl_explorer.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const nodes = {};
const timers = [];
function element() {
  const classes = new Set();
  return {
    children: [], dataset: {}, attributes: {}, value: '10', width: 820, height: 320,
    innerHTML: '', textContent: '',
    classList: {
      add: name => classes.add(name), remove: (...names) => names.forEach(n => classes.delete(n)),
      toggle: (name, on) => on ? classes.add(name) : classes.delete(name),
      contains: name => classes.has(name),
    },
    appendChild(child) { this.children.push(child); },
    setAttribute(name, value) { this.attributes[name] = value; },
    getContext: () => new Proxy({}, { get: () => () => {} }),
  };
}
const sandbox = { Math, setTimeout: callback => timers.push(callback), document: {
  querySelectorAll: () => [], createElement: element,
  getElementById: id => nodes[id] ??= element(),
} };
vm.createContext(sandbox);
vm.runInContext(script, sandbox);

nodes.seed1 = element(); nodes.seed1.value = '42';
nodes.run1.onclick();
const first = nodes.out1.innerHTML;
nodes.run1.onclick();
assert.equal(nodes.out1.innerHTML, first, 'same seed must reproduce the run');
nodes.seed1.value = '43'; nodes.run1.onclick();
assert.notEqual(nodes.out1.innerHTML, first, 'different seed should change this run');

nodes.eps.value = '100'; nodes.run1.onclick();
assert.match(nodes.out1.innerHTML, /fully random/);
assert.match(nodes.out1.innerHTML, /policy ignores/);
assert.doesNotMatch(nodes.out1.innerHTML, /found B|sampling noise/);
assert.match(nodes.chartAlt.textContent, /expectations, not ceilings/);
nodes.compare1.onclick();
assert.match(nodes.out1.innerHTML, /50 finite runs/);
assert.match(nodes.out1.innerHTML, /SD/);
assert.match(nodes.out1.innerHTML, /does not exploit/);

const button = nodes.banners0.children[0];
assert.equal(button.type, 'button');
button.onclick();
assert.equal(nodes.banners0.children[0], button, 'click must preserve focusable button');
assert.ok(button.classList.contains('flash-click') || button.classList.contains('flash-noclick'));
timers.forEach(callback => callback());
assert.ok(!button.classList.contains('flash-click') && !button.classList.contains('flash-noclick'));
assert.match(button.attributes['aria-label'], /shown 1/);

nodes.seed3 = element(); nodes.seed3.value = '42';
nodes.run3.onclick();
assert.match(nodes.out3.innerHTML, /not Q-learning/);
const contextual = nodes.out3.innerHTML;
nodes.run3.onclick(); assert.equal(nodes.out3.innerHTML, contextual);
nodes.reset3.onclick(); assert.equal(nodes.q00.textContent, '—');
nodes.reset1.onclick(); assert.match(nodes.chartAlt.textContent, /no simulation/);
nodes.reset0.onclick(); assert.match(button.attributes['aria-label'], /shown 0/);
console.log('Explorer checks passed: seeds, random policy, comparison, accessible cards, context, resets.');
