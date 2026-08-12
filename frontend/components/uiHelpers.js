export function createCell(text) {
  const cell = document.createElement("td");
  cell.textContent = text;
  return cell;
}

export function createActionButton(label, variant = "primary", onClick) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = `action-button ${variant}`.trim();
  button.textContent = label;
  button.addEventListener("click", onClick);
  return button;
}

export function clearChildren(element) {
  element.innerHTML = "";
}

export function populateSelectOptions(selectElement, items, labelFn) {
  selectElement.innerHTML = "";
  selectElement.appendChild(createOption("", "Select..."));
  items.forEach((item) => {
    selectElement.appendChild(createOption(item.id, labelFn(item)));
  });
}

function createOption(value, label) {
  const option = document.createElement("option");
  option.value = value;
  option.textContent = label;
  return option;
}
