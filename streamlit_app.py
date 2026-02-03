<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <title>공시지가 대비 매매호가 계산기</title>

  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #f4f6f8;
      padding: 40px;
    }

    .calculator {
      max-width: 520px;
      margin: auto;
      background: #fff;
      padding: 24px;
      border-radius: 12px;
      box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }

    h1 {
      font-size: 20px;
      margin-bottom: 20px;
      text-align: center;
    }

    .field {
      margin-bottom: 16px;
    }

    .field label {
      display: block;
      font-size: 14px;
      margin-bottom: 6px;
      color: #333;
    }

    .field input {
      width: 100%;
      padding: 10px;
      font-size: 15px;
      border: 1px solid #ddd;
      border-radius: 6px;
    }

    .unit-select {
      display: flex;
      gap: 12px;
      margin-top: 8px;
      font-size: 14px;
    }

    button {
      width: 100%;
      padding: 14px;
      font-size: 16px;
      background: #2563eb;
      color: #fff;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      margin-top: 10px;
    }

    button:hover {
      background: #1e4fd6;
    }

    .result {
      margin-top: 30px;
      padding-top: 20px;
      border-top: 1px solid #eee;
    }

    .hidden {
      display: none;
    }

    .result p {
      font-size: 15px;
      margin: 6px 0;
    }

    .positive {
      color: #dc2626;
      font-weight: 600;
    }

    .negative {
      color: #2563eb;
      font-weight: 600;
    }

    /* 배터리 블럭 */
    .battery {
      display: flex;
      gap: 6px;
      margin: 16px 0 8px;
    }

    .block {
      width: 32px;
      height: 20px;
      border-radius: 4px;
      background: #e5e7eb;
    }

    .ratio-text {
      font-size: 14px;
      font-weight: bold;
    }

    .warning {
      margin-top: 6px;
      font-size: 13px;
      color: #dc2626;
      font-weight: 600;
    }
  </style>
</head>

<body>
  <div class="calculator">
    <h1>공시지가 대비 매매호가 계산기</h1>

    <!-- 입력 -->
    <div class="field">
      <label>공시지가 (원 / ㎡)</label>
      <input type="text" placeholder="예: 5,000,000" />
    </div>

    <div class="field">
      <label>토지면적</label>
      <input type="text" placeholder="면적 입력" />
      <div class="unit-select">
        <label><input type="radio" name="unit" checked /> ㎡</label>
        <label><input type="radio" name="unit" /> 평</label>
      </div>
    </div>

    <div class="field">
      <label>현재 매매호가 (억원)</label>
      <input type="text" placeholder="예: 18" />
    </div>

    <button>계산하기</button>

    <!-- 결과 -->
    <div class="result hidden">
      <p>공시지가 기준 토지가치: <strong id="landValue"></strong></p>
      <p>현재 매매호가: <strong id="saleValue"></strong></p>
      <p>차이: <strong id="diffValue"></strong></p>

      <div class="battery">
        <div class="block"></div><div class="block"></div><div class="block"></div>
        <div class="block"></div><div class="block"></div><div class="block"></div>
        <div class="block"></div><div class="block"></div><div class="block"></div>
        <div class="block"></div>
      </div>

      <div class="ratio-text" id="ratioText"></div>
      <div class="warning" id="warningText"></div>
    </div>
  </div>

  <!-- JavaScript -->
  <script>
    const button = document.querySelector("button");
    const resultBox = document.querySelector(".result");

    button.addEventListener("click", () => {
      const inputs = document.querySelectorAll("input[type='text']");
      const landPrice = parseNumber(inputs[0].value);
      const landArea = parseNumber(inputs[1].value);
      const salePriceEok = parseNumber(inputs[2].value);

      const unit = document.querySelector("input[name='unit']:checked")
        .parentElement.textContent.trim();

      if (!landPrice || !landArea || !salePriceEok) {
        alert("모든 값을 입력해주세요.");
        return;
      }

      // 토지가치 계산
      const landValue =
        unit === "㎡"
          ? landPrice * landArea
          : landPrice * 3.3058 * landArea;

      // 매매호가 (억원 → 원)
      const saleValue = salePriceEok * 100000000;

      // 차이 / 괴리율
      const diff = saleValue - landValue;
      const ratio = (saleValue / landValue) * 100;

      // 결과 표시
      resultBox.classList.remove("hidden");

      document.getElementById("landValue").innerText = formatWon(landValue);
      document.getElementById("saleValue").innerText = salePriceEok + "억";

      const diffEl = document.getElementById("diffValue");
      diffEl.innerText = formatWon(diff);
      diffEl.className = diff >= 0 ? "positive" : "negative";

      document.getElementById("ratioText").innerText =
        `공시지가 대비 ${ratio.toFixed(1)}%`;

      updateBattery(ratio);
      updateWarning(ratio);
    });

    function parseNumber(value) {
      return Number(value.replace(/,/g, ""));
    }

    function formatWon(value) {
      const abs = Math.abs(value);
      const eok = Math.floor(abs / 100000000);
      const man = Math.floor((abs % 100000000) / 10000);

      let text = "";
      if (eok > 0) text += `${eok}억 `;
      if (man > 0) text += `${man.toLocaleString()}만원`;

      return (value >= 0 ? "+" : "-") + text;
    }

    function updateBattery(ratio) {
      const blocks = document.querySelectorAll(".block");
      const max = blocks.length;
      let filled = Math.round((ratio / 200) * max);
      filled = Math.min(filled, max);

      blocks.forEach((block, i) => {
        if (i < filled) {
          if (ratio <= 100) block.style.background = "#22c55e";
          else if (ratio <= 150) block.style.background = "#facc15";
          else block.style.background = "#ef4444";
        } else {
          block.style.background = "#e5e7eb";
        }
      });
    }

    function updateWarning(ratio) {
      const warning = document.getElementById("warningText");
      warning.innerText =
        ratio > 200 ? "⚠ 공시지가 대비 과도한 프리미엄 구간입니다." : "";
    }

    // 입력 시 콤마 자동
    document.querySelectorAll("input[type='text']").forEach(input => {
      input.addEventListener("input", () => {
        input.value = input.value
          .replace(/,/g, "")
          .replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      });
    });
  </script>
</body>
</html>
