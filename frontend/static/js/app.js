// ---------------- ELEMENTS ----------------
const memeBox = document.getElementById("memeBox");
const amountInput = document.getElementById("amount");
const merchantInput = document.getElementById("merchant");
const categoryInput = document.getElementById("category");
const addBtn = document.getElementById("addExpense");
const messageBox = document.getElementById("message");
const summaryBox = document.getElementById("aiSummary");

// ---------------- AUTO PREDICT CATEGORY ----------------
merchantInput.addEventListener("input", async () => {
  const merchant = merchantInput.value.trim();
  if (merchant.length < 3) return;

  const res = await fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ merchant })
  });

  const data = await res.json();
  categoryInput.value = data.category;
});

// ---------------- ADD EXPENSE ----------------
addBtn.addEventListener("click", async () => {
  const amount = amountInput.value;
  const merchant = merchantInput.value;
  const category = categoryInput.value;

  // ✅ Validation
  if (!amount || !merchant || !category) {
    alert("Please fill all fields");
    return;
  }

  // ✅ Save expense
  await fetch("/add-expense", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ amount, merchant, category })
  });

  messageBox.innerText = "✅ Expense added successfully";

  // ✅ Meme
  const memeRes = await fetch(`/meme/${category}`);
  const memeData = await memeRes.json();
  memeBox.innerText = "😂 " + memeData.meme;

  // ✅ AI Summary
  const summaryRes = await fetch("/summary");
  const summaryData = await summaryRes.json();
  summaryBox.innerHTML = "🧠 <b>AI Summary:</b><br>" + summaryData.summary;

  // ✅ Update chart
  loadChart();

  // ✅ Reset inputs
  amountInput.value = "";
  merchantInput.value = "";
  categoryInput.value = "";
});

// ---------------- LOAD CHART ----------------
async function loadChart() {
  const res = await fetch("/chart-data");
  const data = await res.json();

  const canvas = document.getElementById("categoryChart");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");

  if (window.myChart) {
    window.myChart.destroy();
  }

  window.myChart = new Chart(ctx, {
    type: "pie",
    data: {
      labels: data.labels,
      datasets: [{
        data: data.values,
        backgroundColor: [
          "#60a5fa",
          "#34d399",
          "#f87171",
          "#fbbf24",
          "#a78bfa"
        ]
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            color: "#ffffff"
          }
        },
        datalabels: {
          color: "#ffffff",
          font: {
            weight: "bold",
            size: 14
          },
          formatter: (value) => `₹${value}`
        }
      }
    },
    plugins: [ChartDataLabels]
  });
}

// ---------------- RESET DATA ----------------
document.getElementById("resetBtn").addEventListener("click", async () => {
  if (!confirm("Saara data delete ho jayega 😬 Sure?")) return;

  await fetch("/reset", { method: "POST" });

  messageBox.innerText = "♻ Data reset successfully";
  memeBox.innerText = "";
  summaryBox.innerText = "";

  loadChart();
});

// ---------------- INITIAL LOAD ----------------
loadChart();
