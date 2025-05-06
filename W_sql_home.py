import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import mysql.connector
from mysql.connector import Error

class AdvancedMySQLManager:
    def __init__(self, root):
        self.root = root
        self.root.title("مدير قواعد البيانات المتقدم")
        self.root.geometry("1000x700")
        self.root.minsize(900, 600)
        
        # اتصال قاعدة البيانات
        self.connection = None
        self.current_table = None
        
        # إنشاء واجهة المستخدم
        self.create_main_frames()
        self.create_connection_panel()
        self.create_table_management_panel()
        self.create_data_management_panel()
        self.create_sql_editor_panel()
        
        # حالة البدء
        self.set_startup_state()
    
    def set_startup_state(self):
        """حالة البرنامج عند البدء"""
        self.tables_combobox.set('')
        self.data_tree['columns'] = ['info']
        self.data_tree.heading('info', text='الرجاء الاتصال بقاعدة البيانات أولاً')
    
    def create_main_frames(self):
        """إنشاء الإطارات الرئيسية"""
        # إطار رأس الصفحة
        self.header_frame = ttk.Frame(self.root)
        self.header_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(self.header_frame, text="مدير قواعد البيانات المتقدم", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # إطار المحتوى الرئيسي
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # إطار جانبي للتحكم
        self.sidebar_frame = ttk.Frame(self.main_frame, width=250)
        self.sidebar_frame.pack(side="left", fill="y", padx=(0, 10))
        
        # إطار محتوى البيانات
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True)
  
    ################################################################################################
    def create_connection_panel(self):
        """لوحة اتصال قاعدة البيانات"""
        conn_frame = ttk.LabelFrame(self.sidebar_frame, text="إعدادات الاتصال", padding=10)
        conn_frame.pack(fill="x", pady=(0, 10))
        
        # حقول الإدخال
        fields = [
            ("السيرفر:", "host_entry", "localhost", False),
            ("اسم المستخدم:", "user_entry", "root", False),
            ("كلمة المرور:", "pass_entry", "", True),
            ("قاعدة البيانات:", "db_entry", "QQ", False)
        ]
        
        for label, attr, default, is_password in fields:
            frame = ttk.Frame(conn_frame)
            frame.pack(fill="x", pady=3)
            
            ttk.Label(frame, text=label).pack(side="left")
            entry = ttk.Entry(frame, show="*" if is_password else "")
            entry.pack(side="right", fill="x", expand=True)
            entry.insert(0, default)
            setattr(self, attr, entry)
        
        # أزرار التحكم
            btn_frame = ttk.Frame(conn_frame)
            btn_frame.pack(fill="x", pady=(10, 0))
        
        self.connect_btn = ttk.Button(btn_frame, text="اتصال", command=self.connect_to_db)
        self.connect_btn.pack(fill="x")##

       
    def create_table_management_panel(self):
        """لوحة إدارة الجداول"""
        table_frame = ttk.LabelFrame(self.sidebar_frame, text="إدارة الجداول", padding=10)
        table_frame.pack(fill="x", pady=(0, 10))
        
        # زر تحديث الجداول
        ttk.Button(table_frame, text="تحديث قائمة الجداول", command=self.refresh_tables).pack(fill="x", pady=3)
        
        # قائمة الجداول
        ttk.Label(table_frame, text="الجداول المتاحة:").pack(anchor="w", pady=(10, 3))
        self.tables_combobox = ttk.Combobox(table_frame, state="readonly")
        self.tables_combobox.pack(fill="x", pady=3)
        self.tables_combobox.bind("<<ComboboxSelected>>", self.load_table_data)
        
        # أزرار إدارة الجداول
        btn_frame = ttk.Frame(table_frame)
        btn_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(btn_frame, text="إنشاء جدول", command=self.create_new_table_dialog).pack(side="left", fill="x", expand=True, padx=2)
        ttk.Button(btn_frame, text="حذف جدول", command=self.delete_table).pack(side="right", fill="x", expand=True, padx=2)
    
    def create_data_management_panel(self):
        """لوحة إدارة البيانات"""
        # إطار عرض البيانات
        data_display_frame = ttk.LabelFrame(self.content_frame, text="عرض البيانات", padding=10)
        data_display_frame.pack(fill="both", expand=True)
        
        # شجرة البيانات
        self.data_tree = ttk.Treeview(data_display_frame)
        self.data_tree.pack(fill="both", expand=True, side="left")
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(data_display_frame, orient="vertical", command=self.data_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.data_tree.configure(yscrollcommand=scrollbar.set)
        
        # إطار أدوات التحكم
        control_frame = ttk.Frame(self.content_frame, padding=10)
        control_frame.pack(fill="x", pady=(10, 0))
        
        # أزرار التحكم بالبيانات
        ttk.Button(control_frame, text="إضافة صف جديد", command=self.add_row).pack(side="left", padx=3)
        ttk.Button(control_frame, text="تعديل الصف المحدد", command=self.edit_row).pack(side="left", padx=3)
        ttk.Button(control_frame, text="حذف الصف المحدد", command=self.delete_row).pack(side="left", padx=3)
    
    def create_sql_editor_panel(self):
        """لوحة محرر SQL"""
        sql_frame = ttk.LabelFrame(self.content_frame, text="محرر SQL", padding=10)
        sql_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # محرر نصوص للاستعلامات SQL
        self.sql_editor = scrolledtext.ScrolledText(sql_frame, height=8, font=('Courier New', 10))
        self.sql_editor.pack(fill="both", expand=True)
        
        # أزرار تنفيذ الاستعلام
        btn_frame = ttk.Frame(sql_frame)
        btn_frame.pack(fill="x", pady=(5, 0))
        
        ttk.Button(btn_frame, text="تنفيذ", command=self.execute_sql).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="مسح", command=self.clear_sql_editor).pack(side="left", padx=2)
    
    def connect_to_db(self):
        """الاتصال بقاعدة البيانات"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host_entry.get(),
                user=self.user_entry.get(),
                password=self.pass_entry.get(),
                database=self.db_entry.get(),
                auth_plugin='mysql_native_password'
            )
            
            messagebox.showinfo("نجاح", "تم الاتصال بنجاح بقاعدة البيانات!")
            self.connect_btn.config(text="تنشيط", state="") #  تم تعطيل هذا السطر لانه يمنع التنقل الي قاعده بيانات اخري 
            self.refresh_tables()
            
        except Error as e:
            messagebox.showerror("خطأ في الاتصال", f"فشل الاتصال بقاعدة البيانات:\n{str(e)}")
    
    def refresh_tables(self):
        """تحديث قائمة الجداول"""
        if not self.connection:
            return
            
        try:
            cursor = self.connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor]
            
            self.tables_combobox['values'] = tables
            if tables:
                self.tables_combobox.current(0)
                self.load_table_data()
                
        except Error as e:
            messagebox.showerror("خطأ", f"فشل جلب الجداول:\n{str(e)}")
    
    def create_new_table_dialog(self):
        """نافذة إنشاء جدول جديد مع خيارين"""
        dialog = tk.Toplevel(self.root)
        dialog.title("إنشاء جدول جديد")
        dialog.geometry("600x450")

        # إنشاء تبويبات
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill="both", expand=True)

        # تبويب الواجهة الرسومية
        gui_frame = ttk.Frame(notebook)
        notebook.add(gui_frame, text="واجهة رسومية")

        # تبويب المحرر اليدوي
        sql_frame = ttk.Frame(notebook)
        notebook.add(sql_frame, text="كتابة يدوية")

        # محتوى تبويب الواجهة الرسومية
        ttk.Label(gui_frame, text="اسم الجدول:").pack(pady=(10, 0))
        table_name_entry = ttk.Entry(gui_frame)
        table_name_entry.pack(fill="x", padx=20, pady=5)

        ttk.Label(gui_frame, text="تعريف الأعمدة:").pack(pady=(10, 0))
        columns_editor = scrolledtext.ScrolledText(gui_frame, height=10, font=('Courier New', 10))
        columns_editor.pack(fill="both", expand=True, padx=20, pady=5)
        columns_editor.insert("1.0", "id INT AUTO_INCREMENT PRIMARY KEY,\nname VARCHAR(100),\nage INT")

        # محتوى تبويب الكتابة اليدوية
        sql_editor = scrolledtext.ScrolledText(sql_frame, height=15, font=('Courier New', 10))
        sql_editor.pack(fill="both", expand=True, padx=20, pady=10)
        sql_editor.insert("1.0", "CREATE TABLE table_name (\n    column1 datatype,\n    column2 datatype\n)")

        # أزرار التنفيذ المشتركة
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill="x", padx=20, pady=10)

        def create_table():
            current_tab = notebook.index(notebook.select())
            
            if current_tab == 0:  # الواجهة الرسومية
                table_name = table_name_entry.get().strip()
                columns_def = columns_editor.get("1.0", tk.END).strip()
                
                if not table_name or not columns_def:
                    messagebox.showwarning("تحذير", "الرجاء إدخال اسم الجدول وتعريف الأعمدة")
                    return
                    
                sql = f"CREATE TABLE {table_name} ({columns_def})"
                
            else:  # المحرر اليدوي
                sql = sql_editor.get("1.0", tk.END).strip()
                if not sql.upper().startswith("CREATE TABLE"):
                    messagebox.showwarning("تحذير", "الاستعلام يجب أن يبدأ بـ CREATE TABLE")
                    return

            try:
                cursor = self.connection.cursor()
                cursor.execute(sql)
                self.connection.commit()
                messagebox.showinfo("نجاح", "تم إنشاء الجدول بنجاح!")
                dialog.destroy()
                self.refresh_tables()
                
            except Error as e:
                messagebox.showerror("خطأ", f"فشل إنشاء الجدول:\n{str(e)}")

        ttk.Button(btn_frame, text="إنشاء", command=create_table).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="إلغاء", command=dialog.destroy).pack(side="left", padx=5)
    
    def delete_table(self):
        """حذف جدول"""
        table_name = self.tables_combobox.get()
        if not table_name:
            return
            
        if not messagebox.askyesno("تأكيد الحذف", f"هل أنت متأكد من حذف الجدول {table_name}؟"):
            return
            
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"DROP TABLE {table_name};")
            self.connection.commit()
            messagebox.showinfo("نجاح", f"تم حذف الجدول {table_name} بنجاح!")
            self.refresh_tables()
            
        except Error as e:
            messagebox.showerror("خطأ", f"فشل حذف الجدول:\n{str(e)}")
    
    def load_table_data(self, event=None):
        """تحميل بيانات الجدول المحدد"""
        self.current_table = self.tables_combobox.get()
        if not self.current_table:
            return
            
        try:
            cursor = self.connection.cursor()
            
            # جلب أسماء الأعمدة
            cursor.execute(f"DESCRIBE {self.current_table}")
            columns = [column[0] for column in cursor.fetchall()]
            
            # جلب البيانات
            cursor.execute(f"SELECT * FROM {self.current_table}")
            data = cursor.fetchall()
            
            # تحديث شجرة البيانات
            self.update_data_tree(columns, data)
            
        except Error as e:
            messagebox.showerror("خطأ", f"فشل تحميل البيانات:\n{str(e)}")
    
    def update_data_tree(self, columns, data):
        """تحديث شجرة البيانات"""
        # مسح البيانات القديمة
        self.data_tree.delete(*self.data_tree.get_children())
        
        # إعداد الأعمدة
        self.data_tree['columns'] = columns
        for col in columns:
            self.data_tree.heading(col, text=col)
            self.data_tree.column(col, width=120, minwidth=50, anchor='center')
        
        # إضافة البيانات
        for row in data:
            self.data_tree.insert("", "end", values=row)
    
    def add_row(self):
        """إضافة صف جديد"""
        if not self.current_table:
            messagebox.showwarning("تحذير", "الرجاء تحديد جدول أولاً")
            return
            
        try:
            cursor = self.connection.cursor()
            
            # جلب أسماء الأعمدة وأنواعها
            cursor.execute(f"DESCRIBE {self.current_table}")
            columns_info = cursor.fetchall()
            
            # إنشاء نافذة إدخال البيانات
            dialog = tk.Toplevel(self.root)
            dialog.title("إضافة صف جديد")
            dialog.geometry("400x300")
            
            entries = {}
            for i, (column, type_, *_) in enumerate(columns_info):
                frame = ttk.Frame(dialog, padding=5)
                frame.pack(fill="x")
                
                ttk.Label(frame, text=f"{column} ({type_}):").pack(side="left")
                entry = ttk.Entry(frame)
                entry.pack(side="right", fill="x", expand=True)
                entries[column] = entry
            
            def save_new_row():
                try:
                    # بناء استعلام الإدراج
                    columns = ", ".join(entries.keys())
                    placeholders = ", ".join(["%s"] * len(entries))
                    values = [entry.get() for entry in entries.values()]
                    
                    cursor.execute(
                        f"INSERT INTO {self.current_table} ({columns}) VALUES ({placeholders})",
                        values
                    )
                    cursor.execute.upper()
                    self.connection.commit()
                    messagebox.showinfo("نجاح", "تمت إضافة الصف بنجاح!")
                    dialog.destroy()
                    self.load_table_data()
                    
                except Error as e:
                    messagebox.showerror("خطأ", f"فشل إضافة الصف:\n{str(e)}")
            
            ttk.Button(dialog, text="حفظ", command=save_new_row).pack(pady=10)
            
        except Error as e:
            messagebox.showerror("خطأ", f"فشل جلب معلومات الجدول:\n{str(e)}")
    
    def edit_row(self):
        """تعديل صف موجود"""
        selected_item = self.data_tree.selection()
        if not selected_item:
            messagebox.showwarning("تحذير", "الرجاء تحديد صف لتعديله")
            return
            
        try:
            cursor = self.connection.cursor()
            
            # جلب أسماء الأعمدة وأنواعها
            cursor.execute(f"DESCRIBE {self.current_table}")
            columns_info = cursor.fetchall()
            
            # جلب بيانات الصف المحدد
            item_data = self.data_tree.item(selected_item)['values']
            
            # إنشاء نافذة التعديل
            dialog = tk.Toplevel(self.root)
            dialog.title("تعديل الصف")
            dialog.geometry("400x300")
            
            entries = {}
            for i, (column, type_, *_) in enumerate(columns_info):
                frame = ttk.Frame(dialog, padding=5)
                frame.pack(fill="x")
                
                ttk.Label(frame, text=f"{column} ({type_}):").pack(side="left")
                entry = ttk.Entry(frame)
                entry.pack(side="right", fill="x", expand=True)
                entry.insert(0, str(item_data[i]))
                entries[column] = entry
            
            def save_edited_row():
                try:
                    # بناء استعلام التحديث
                    set_clause = ", ".join([f"{col} = %s" for col in entries.keys()])
                    values = [entry.get() for entry in entries.values()]
                    primary_key = columns_info[0][0]  # نفترض أن العمود الأول هو المفتاح الأساسي
                    primary_value = item_data[0]
                    
                    cursor.execute(
                        f"UPDATE {self.current_table} SET {set_clause} WHERE {primary_key} = %s",
                        values + [primary_value]
                    )
                    self.connection.commit()
                    messagebox.showinfo("نجاح", "تم تعديل الصف بنجاح!")
                    dialog.destroy()
                    self.load_table_data()
                    
                except Error as e:
                    messagebox.showerror("خطأ", f"فشل تعديل الصف:\n{str(e)}")
            
            ttk.Button(dialog, text="حفظ التعديلات", command=save_edited_row).pack(pady=10)
            
        except Error as e:
            messagebox.showerror("خطأ", f"فشل تحرير الصف:\n{str(e)}")
    
    def delete_row(self):
        """حذف صف"""
        selected_item = self.data_tree.selection()
        if not selected_item:
            messagebox.showwarning("تحذير", "الرجاء تحديد صف لحذفه")
            return
            
        if not messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد من حذف هذا الصف؟"):
            return
            
        try:
            cursor = self.connection.cursor()
            
            # جلب اسم العمود الأساسي
            cursor.execute(f"DESCRIBE {self.current_table}")
            primary_key = cursor.fetchall()[0][0]  # نفترض أن العمود الأول هو المفتاح الأساسي
            
            # جلب قيمة المفتاح الأساسي للصف المحدد
            primary_value = self.data_tree.item(selected_item)['values'][0]
            
            # تنفيذ عملية الحذف
            cursor.execute(
                f"DELETE FROM {self.current_table} WHERE {primary_key} = %s",
                (primary_value,)
            )
            self.connection.commit()
            messagebox.showinfo("نجاح", "تم حذف الصف بنجاح!")
            self.load_table_data()
            
        except Error as e:
            messagebox.showerror("خطأ", f"فشل حذف الصف:\n{str(e)}")
    
    def execute_sql(self):
        """تنفيذ استعلام SQL"""
        sql = self.sql_editor.get("1.0", tk.END).strip()
        if not sql:
            messagebox.showwarning("تحذير", "الرجاء إدخال استعلام SQL")
            return
            
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            
            if sql.strip().upper().startswith("SELECT"):
                # عرض نتائج SELECT
                columns = [desc[0] for desc in cursor.description]
                data = cursor.fetchall()
                
                result_window = tk.Toplevel(self.root)
                result_window.title("نتيجة الاستعلام")
                
                tree = ttk.Treeview(result_window, columns=columns, show="headings")
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=100)
                
                for row in data:
                    tree.insert("", "end", values=row)
                
                tree.pack(fill="both", expand=True)
            else:
                # تنفيذ استعلامات غير SELECT
                self.connection.commit()
                messagebox.showinfo("نجاح", f"تم تنفيذ الاستعلام بنجاح!\nعدد الصفوف المتأثرة: {cursor.rowcount}")
                self.refresh_tables()
                
        except Error as e:
            messagebox.showerror("خطأ", f"فشل تنفيذ الاستعلام:\n{str(e)}")
    
    def clear_sql_editor(self):
        """مسح محرر SQL"""
        self.sql_editor.delete("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedMySQLManager(root)
    root.mainloop()