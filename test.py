import pandas as pd
import numpy as np
import openpyxl
import matplotlib.pyplot as plt
import seaborn as sns
import scipy

print("✅ כל הספריות עובדות!")
print(f"Pandas: {pd.__version__}")
print(f"Numpy: {np.__version__}")
print(f"Openpyxl: {openpyxl.__version__}")

# בדיקה מהירה - יצירת DataFrame
df = pd.DataFrame({
    'שם': ['רותם', 'עובד 1', 'עובד 2'],
    'ציון': [95, 87, 92]
})

print("\n", df)

# בדיקות נוספות
print("\n📊 בדיקות נוספות:")

# חישובים עם Numpy
arr = np.array([1, 2, 3, 4, 5])
print(f"ממוצע: {np.mean(arr)}")
print(f"סטיית תקן: {np.std(arr)}")

# סטטיסטיקות של DataFrame
print(f"\nסטטיסטיקות הציונים:\n{df['ציון'].describe()}")

# יצירת סדרה עם Pandas
dates = pd.date_range('2024-01-01', periods=5)
print(f"\nטווח תאריכים:\n{dates}")

# בדיקת Scipy
from scipy import stats
print(f"\nחציון (scipy): {stats.median_abs_deviation([1,2,3,4,5])}")

# יצירת נתונים אקראיים
random_data = np.random.randn(3, 3)
print(f"\nמטריצה אקראית:\n{random_data}")

print("\n✅ כל הבדיקות הסתיימו בהצלחה!")

# קריאת קובץ Excel עם pandas
# החלף את 'path/to/your/file.xlsx' בנתיב האמיתי לקובץ
try:
    df_excel = pd.read_excel('path/to/your/file.xlsx')
    print("\n📄 קריאת קובץ Excel הצליחה!")
    print(f"מספר שורות: {len(df_excel)}")
    print(f"מספר עמודות: {len(df_excel.columns)}")
    print(f"שמות העמודות: {list(df_excel.columns)}")
    print("\nראש 5 שורות:")
    print(df_excel.head())
except FileNotFoundError:
    print("\n❌ קובץ Excel לא נמצא. החלף את הנתיב ב-'path/to/your/file.xlsx'")
except Exception as e:
    print(f"\n❌ שגיאה בקריאת קובץ Excel: {e}")

# cd ~/analytics_work
# source venv/bin/activate

# python test.py