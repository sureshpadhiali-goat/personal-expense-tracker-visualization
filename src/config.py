"""Central settings: paths, categories, budgets."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
IMAGES_DIR = ROOT / "images"
REPORTS_DIR = ROOT / "reports"
RAW_CSV = DATA_DIR / "expenses_raw.csv"
CLEAN_CSV = DATA_DIR / "expenses_clean.csv"
DB_PATH = DATA_DIR / "expenses.db"

# Monthly budget per category (INR) - edit freely
BUDGETS = {
    "Food": 6000, "Rent": 12000, "Transport": 2500, "Shopping": 3000,
    "Bills": 3500, "Entertainment": 2000, "Health": 1500, "Education": 2000,
}
MONTHLY_INCOME = 50000

# Keyword rules for auto-categorizing a note when category is missing
CATEGORY_KEYWORDS = {
    "Food": ["swiggy", "zomato", "restaurant", "grocery", "cafe", "lunch", "dinner", "tea"],
    "Rent": ["rent", "pg", "landlord"],
    "Transport": ["uber", "ola", "metro", "bus", "fuel", "petrol", "auto"],
    "Shopping": ["amazon", "flipkart", "myntra", "clothes", "shoes"],
    "Bills": ["electricity", "wifi", "recharge", "water", "gas"],
    "Entertainment": ["movie", "netflix", "spotify", "game", "concert"],
    "Health": ["pharmacy", "doctor", "medicine", "gym"],
    "Education": ["course", "book", "udemy", "exam", "tuition"],
}
