import os
import sqlite3

dbConn = None


def dbConnection():
    global dbConn
    os.makedirs("Database", exist_ok=True)
    dbConn = sqlite3.connect("Database/test.db")


def createTable():
    if dbConn is None:
        dbConnection()

    dbCursor = dbConn.cursor()
    sqlStr = """SELECT count(name)
    FROM sqlite_master
    WHERE type='table' AND name='Students';
    """
    dbCursor.execute(sqlStr)

    if dbCursor.fetchone()[0] == 1:
        print("Table 'Students' already exists.")
    else:
        sqlStr = """CREATE TABLE Students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gender TEXT NOT NULL,
            department TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            address TEXT
        );"""
        dbCursor.execute(sqlStr)
        dbConn.commit()
        print("Table 'Students' created.")


def find_student_by_email(email):
    if dbConn is None:
        dbConnection()

    dbCursor = dbConn.cursor()
    dbCursor.execute("SELECT * FROM Students WHERE email = ?", (email,))
    return dbCursor.fetchone()


def insert_student(name, gender, department, email, phone, address):
    if dbConn is None:
        dbConnection()

    dbCursor = dbConn.cursor()

    if find_student_by_email(email) is None:
        dbCursor.execute(
            """INSERT INTO Students (name, gender, department, email, phone, address)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (name, gender, department, email, phone, address),
        )
        dbConn.commit()
        print(f"[成功] 已新增學生 {name}")
    else:
        print(f"[錯誤] Email '{email}' 已經被註冊過，請確認後再試！")


def list_all_students():
    if dbConn is None:
        dbConnection()

    dbCursor = dbConn.cursor()
    dbCursor.execute("SELECT * FROM Students")
    students = dbCursor.fetchall()

    print("\n=== All Students ===")
    if not students:
        print("目前沒有任何學生資料。")
        return

    print(
        f"{'ID':<4} | {'姓名':<10} | {'性別':<6} | {'系所':<10} | {'Email':<30} | {'電話':<12}"
    )
    print("-" * 90)

    for student in students:
        print(
            f"{student[0]:<4} | {student[1]:<10} | {student[2]:<6} | {student[3]:<10} | {student[4]:<30} | {student[5]:<12}"
        )

    print("-" * 90)


def search_student_by_id(student_id):
    if dbConn is None:
        dbConnection()

    dbCursor = dbConn.cursor()
    dbCursor.execute("SELECT * FROM Students WHERE id = ?", (student_id,))
    return dbCursor.fetchone()


def update_student(student_id, phone, address):
    if dbConn is None:
        dbConnection()

    dbCursor = dbConn.cursor()
    dbCursor.execute(
        "UPDATE Students SET phone = ?, address = ? WHERE id = ?",
        (phone, address, student_id),
    )
    dbConn.commit()

    if dbCursor.rowcount > 0:
        print(f"[成功] 已更新學生 ID {student_id}")
    else:
        print("[失敗] 找不到學生")


def delete_student(student_id):
    if dbConn is None:
        dbConnection()

    dbCursor = dbConn.cursor()
    dbCursor.execute("DELETE FROM Students WHERE id = ?", (student_id,))
    dbConn.commit()

    if dbCursor.rowcount > 0:
        print(f"[成功] 已刪除學生 ID {student_id}")
    else:
        print("[失敗] 找不到學生")


def count_students_by_department():
    if dbConn is None:
        dbConnection()

    dbCursor = dbConn.cursor()
    dbCursor.execute(
        """SELECT department, COUNT(*)
        FROM Students
        GROUP BY department"""
    )
    results = dbCursor.fetchall()

    print("\n=== 📊 系所人數統計 ===")
    if not results:
        print("目前沒有任何學生資料。")
        return

    print(f"{'系所名稱':<12} | {'人數':<5}")
    print("-" * 22)
    for row in results:
        print(f"{row[0]:<12} | {row[1]:<5}")
    print("-" * 22)


def fuzzy_search_students(keyword):
    if dbConn is None:
        dbConnection()

    dbCursor = dbConn.cursor()
    dbCursor.execute(
        """SELECT id, name, department, address
        FROM Students
        WHERE name LIKE ? OR address LIKE ?""",
        (f"%{keyword}%", f"%{keyword}%"),
    )
    return dbCursor.fetchall()


def show_student_detail(student_id):
    student = search_student_by_id(student_id)

    if student is None:
        print("[失敗] 查無資料")
    else:
        print(f"\n=== 📄 學生詳細資料 (ID: {student[0]}) ===")
        print(f"姓名      : {student[1]}")
        print(f"性別      : {student[2]}")
        print(f"系所      : {student[3]}")
        print(f"Email     : {student[4]}")
        print(f"電話      : {student[5]}")
        print(f"地址      : {student[7]}")
        print(f"建檔時間  : {student[6]}")
        print("=" * 35)


def input_student_data():
    print("\n請輸入學生資料")
    name = input("姓名: ")
    gender = input("性別: ")
    department = input("系所: ")
    email = input("Email: ")
    phone = input("電話: ")
    address = input("地址(可空白): ")
    return name, gender, department, email, phone, address


def menu():
    print("\n====================================================")
    print("🏫 學生學籍管理系統（v2.0）")
    print("====================================================")
    print("【基礎維護】")
    print("1. 新增學生資料")
    print("2. 列出所有學生")
    print("3. 修改學生資料（電話 / 地址）")
    print("4. 刪除學生資料")
    print("【進階功能】")
    print("5. 系所人數統計")
    print("6. 關鍵字模糊搜尋（姓名 / 地址）")
    print("7. 查詢單筆詳細資料（依 ID）")
    print("----------------------------------------------------")
    print("0. 登出並關閉系統")
    print("====================================================")


def main():
    dbConnection()
    createTable()

    while True:
        menu()
        choice = input("👉 請選擇功能操作(0-7): ")

        if choice == "1":
            name, gender, department, email, phone, address = input_student_data()
            insert_student(name, gender, department, email, phone, address)

        elif choice == "2":
            list_all_students()

        elif choice == "3":
            try:
                sid = int(input("請輸入學生 ID: "))
                student = search_student_by_id(sid)

                if student is None:
                    print("[失敗] 查無資料")
                else:
                    print(f"\n[目前學生] {student[1]} (ID: {student[0]})")
                    print(f"原電話：{student[5]}")
                    print(f"原地址：{student[7]}")

                    new_phone = input("請輸入新電話（不修改直接 Enter）: ")
                    new_address = input("請輸入新地址（不修改直接 Enter）: ")

                    if new_phone == "":
                        new_phone = student[5]
                    if new_address == "":
                        new_address = student[7]

                    update_student(sid, new_phone, new_address)

            except ValueError:
                print("ID 必須是數字")

        elif choice == "4":
            try:
                sid = int(input("請輸入要刪除的學生 ID: "))
                student = search_student_by_id(sid)

                if student is None:
                    print("[失敗] 查無資料")
                else:
                    confirm = input(
                        f"[警告] 您確定要刪除學生 '{student[1]}' 的資料嗎？(Y/N): "
                    )
                    if confirm.upper() == "Y":
                        delete_student(sid)
                    else:
                        print("已取消刪除")

            except ValueError:
                print("ID 必須是數字")

        elif choice == "5":
            count_students_by_department()

        elif choice == "6":
            keyword = input("請輸入搜尋關鍵字: ")
            results = fuzzy_search_students(keyword)

            print(f"\n=== 🔍 搜尋結果（關鍵字：'{keyword}'）===")
            if not results:
                print("查無符合資料")
            else:
                for row in results:
                    print(
                        f"ID: {row[0]} | 姓名: {row[1]} | 系所: {row[2]} | 地址: {row[3]}"
                    )

        elif choice == "7":
            try:
                sid = int(input("請輸入要查詢的學生 ID: "))
                show_student_detail(sid)
            except ValueError:
                print("ID 必須是數字")

        elif choice == "0":
            print("系統已關閉")
            break

        else:
            print("請輸入 0~7")

    dbConn.close()


if __name__ == "__main__":
    main()
