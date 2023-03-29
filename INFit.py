# %%
#GUI Libs
import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog
import tkinter.ttk as ttk
from tkinter import *

#Py/Utils Libs
from copy import deepcopy
import pickle
import itertools
import os.path




# Model
class Plan:
    def __init__(self, plan_type, price):
        self.name = plan_type
        self.price = price
        
    def __eq__(self, other): 
        if not isinstance(other, Plan):
            return NotImplemented
        return self.name == other.name
    
    def __str__(self):
        return f'Plano {self.name} - Preço: R$ {self.price}'
    
        
class IndividualClass:
    def __init__(self, class_name, price, date):
        self.name = class_name
        self.price = price
        self.date = date
        
    def __eq__(self, other): 
        if not isinstance(other, IndividualClass):
            return NotImplemented
        return self.name == other.name
    
    def __str__(self):
        return f'{self.name} - Dia {self.date} - Preço: R$ {self.price}'
    
    
class Train:
    def __init__(self, exercises):
        self.exercises = exercises

    def __str__(self):
        return f'{self.exercises}'
    
    
class Student:
    def __init__(self, name, balance = 0, cpf = None, age = None, plans = [], classes = [], treinos = []):
        self.name = name
        self.balance = balance
        self.cpf = cpf
        self.age = age
        self.plans = plans
        self.classes = classes
        self.treinos = treinos
        
    def purchase_plan(self, plan):
        if self.balance >= plan.price:
            self.balance -= plan.price
            self.plans.append(plan)
            return True
        return False
    
    def purchase_class(self, indiv_class):
        if self.balance >= int(indiv_class.price):
            self.balance -= int(indiv_class.price)
            self.classes.append(indiv_class)
            return True
        return False

    def balance_add(self, amount):
        try:
            amount = int(amount)
            self.balance+=amount
            return True
        except:
            return False

    def get_balance(self):
        return self.balance

    
    
    
class Login:
    id_iter = itertools.count()
    def __init__(self, username, password, login_type):
        id_iter = itertools.count()
        self.username = username
        self.password = password
        self.login_type = login_type
        self.client_id = next(self.id_iter)
    
    def __eq__(self, other): 
        if not isinstance(other, Login):
            return NotImplemented

        return self.username == other.username



# View

class LoginScreen:
    def __init__(self, master=None):
        self.master = master
        master.title("Login")

        self.username_label = tk.Label(root, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10)

        self.username_entry = tk.Entry(root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10)

        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        self.login_button = tk.Button(root, text="Login", command=self.autenticate_login)
        self.login_button.grid(row=2, column=0, pady=10)

        self.create_button = tk.Button(root, text="Create Account", command=self.create_account)
        self.create_button.grid(row=2, column=1, pady=10)
        

    def create_account(self):

        with open('logins.bin', 'rb+')  as f:
            list_logins = pickle.load(f)

        username = self.username_entry.get()
        if len(username)<3:
            self.master.withdraw()
            messagebox.showinfo("Criar conta falhou", "Username tem que ser maior que 3 caracteres")
            self.master.deiconify()
            return 0
            
        password = self.password_entry.get()
        if len(password)<3:
            self.master.withdraw()
            messagebox.showinfo("Criar conta falhou", "Password tem que ser maior que 3 caracteres")
            self.master.deiconify()
            return 0
            
        login_type = 'user'

        data = Login(username, password, login_type)
        if data not in list_logins:
            list_logins.append(data)
        else:
            self.master.withdraw()
            messagebox.showinfo("Criar Conta falhou", "Username já existe, tente outro")
            self.master.deiconify()
            return 0

        with open('logins.bin', 'wb')  as f:
            pickle.dump(list_logins, f)

        self.master.withdraw()
        messagebox.showinfo("Criar Conta", "Conta criada com sucesso")
        self.master.deiconify()


    def autenticate_login(self):
        list_logins = []

        with open('logins.bin', 'rb+')  as f:
            list_logins = pickle.load(f)

        username = self.username_entry.get()
        if len(username)<3:
            self.master.withdraw()
            messagebox.showinfo("Login falhou", "Username tem que ser maior que 3 caracteres")
            self.master.deiconify()
            return 0
            
        password = self.password_entry.get()
        if len(password)<3:
            self.master.withdraw()
            messagebox.showinfo("Login falhou", "Password tem que ser maior que 3 caracteres")
            self.master.deiconify()
            return 0

        for login in list_logins:
            if login.username == username and login.password == password:
                self.master.withdraw()
                messagebox.showinfo("Login Ok", "Você logou como {}".format(login.login_type))
                if login.login_type == 'student' or login.login_type == 'user':
                    student_view = StudentView(self.master, login.username)
                if login.login_type == 'trainer':
                    student_view = TrainerView(self.master, login.username)
                if login.login_type == 'manager':
                    student_view = ManagerView(self.master, login.username)
                    # student_view = ManagerView()
                break
        else:
            self.master.withdraw()
            messagebox.showinfo("Login Falhou", "Usuário ou senha inválidos")
            self.master.deiconify() 
            
            
            
class StudentView(tk.Toplevel):
    def __init__(self, master, username):
        
        self.first = True
        
        super().__init__(master)


        new_student = True
        for i in list_of_students:
            if i.name == username:
                self.user = i
                new_student = False

        if new_student:
            self.user = Student(username)
            list_of_students.append(self.user)
        
        self.controller = StudentController(self.user, self)
        
        # self.geometry("3000x3000")
        self.title("INFit")
        

        # nome do estudante direita em cima
        username_label = tk.Label(self, text=f"Olá {username}", font=("TkDefaultFont", 12), anchor="e")
        username_label.pack(side="top", fill="x", pady=(10,0))

        self.balanceHolder = tk.IntVar()
        self.textBalanceHolder = tk.StringVar()

        self.update_balance_info()

        balance_label = tk.Label(self,textvariable = self.textBalanceHolder, font=("TkDefaultFont", 12), anchor="e")
        balance_label.pack(side="top", fill="x", pady=(0,0))

        # botão para sair
        quit_button = tk.Button(self, text="Logout", command=self.close_all, anchor="e")
        quit_button.pack(side="right", pady=(0,900))

        # botão de compra de planos/aula
        purchase_plan_button = tk.Button(self, text="Comprar planos ou aulas", font=("TkDefaultFont", 12), command = self.purchasse_command)
        purchase_plan_button.pack(side="right", padx=(10, 20), pady=(50, 10))

        update_balance_button = tk.Button(self, text="Adicionar saldo", font=("TkDefaultFont", 12), command = self.update_balance)
        update_balance_button.pack(side="right", padx=(10, 20), pady=(50, 10))

        # lista com os planos/aulas que você já têm
        already_purchased_label = tk.Label(self, text="Planos e aulas comprados:", font=("TkDefaultFont", 14), anchor="w")
        already_purchased_label.pack(side="top", fill="x", pady=(40,0))

        self.purchased_list = tk.Listbox(self, font=("TkDefaultFont", 12))
        self.purchased_list.pack(side="top", fill = 'x')


        self.assigned_trains_canvas = tk.Listbox(self, font=("TkDefaultFont", 12))
        self.assigned_trains_canvas.pack(side="bottom", fill = 'x')

        assigned_trains_label = tk.Label(self, text="Seus treinos:", font=("TkDefaultFont", 14))
        assigned_trains_label.pack(side="bottom", fill="x", pady=(40,0))


        self.update_purchassed_classes()


    def update_balance_info(self):
        self.balanceHolder.set(self.controller.get_student_balance())
        self.textBalanceHolder.set("Seu saldo: R$:{}.00".format(self.balanceHolder.get()))

    def update_purchassed_classes(self):
        for i in self.user.classes:
            self.purchased_list.insert('end', i)

        for i in self.user.plans:
            self.purchased_list.insert('end', i)

        for i in self.user.treinos:
            self.assigned_trains_canvas.insert('end', i)



    def close_all(self):
        self.withdraw()
        self.master.quit()
        self.master.destroy()

    def purchasse_command(self):
        if self.first:
            varHolder = tk.StringVar()
            self.class_plan_cb = ttk.Combobox(self, textvariable=varHolder)

            all_options = self.controller.get_classes_and_plans()

            self.class_plan_cb['values'] = all_options

            # somente leitura para usuário nao escrever coisa q n existe, intromedito vai estragar o sistema 
            self.class_plan_cb['state'] = 'readonly'
            
            already_purchased_label = tk.Label(self, text="Planos e aulas disponíveis para compra\nClique novamente em comprar planos ou aulas para efetivar a compra:")
            already_purchased_label.pack(pady=10)
            self.class_plan_cb.pack(fill=tk.X, padx=6, pady=6)


            
            self.first = False
        else:
            status_buy = False
            
            all_options = self.controller.get_classes_and_plans()
                        
            value = self.class_plan_cb.current()
            
            if value == -1:
                messagebox.showinfo("Compra falhou", "Selecione uma opção do menu abaixo das aulas disponíveis")
                return 0

            value = all_options[value]


            if str(value) in self.purchased_list.get(0,tk.END):
                messagebox.showinfo("Compra falhou", "Você já comprou esse plano ou aula")
                return 0

            if isinstance(value, Plan):
                if self.controller.purchase_plan(value) == True:
                    status_buy = True
                else:
                    messagebox.showinfo("Compra falhou", "Saldo insuficiente")
                
            elif isinstance(value, IndividualClass):
                if self.controller.purchase_class(value) == True:
                    status_buy = True
                else:
                    messagebox.showinfo("Compra falhou", "Saldo insuficiente")
                    
                
            if status_buy:
                self.purchased_list.insert('end', value)
                self.update_balance_info()

    def update_balance(self):
        amount = tk.simpledialog.askstring("Sistema do Banco de mentirinha", "Valor para depósito: ", parent = self)
        if self.controller.update_balance(amount):
            messagebox.showinfo("Sistema do Banco de mentirinha", "Valor foi depositado corretamente!")
        else:
            messagebox.showinfo("Sistema do Banco de mentirinha", "Cartão recusado!")
        self.balanceHolder.set(self.controller.get_student_balance())
        self.update_balance_info()

class ManagerView(tk.Toplevel):
    def __init__(self, master, username):
        print('rteste')
        self.first = True

        super().__init__(master)

        self.controller = ManagerController(self)
        # self.geometry("1280x1280")
        self.title("INFit - Manager")

        # nome do estudante direita em cima
        username_label = tk.Label(self, text=f"Olá Manager {username}", font=("TkDefaultFont", 12), anchor="e")
        username_label.pack(side="top", fill="x", pady=(10, 0))

        # botão para sair
        quit_button = tk.Button(self, text="Logout", command=self.close_all, anchor="e")
        quit_button.pack(side="right", pady=(0,970))

        # botão de geração de relatório
        request_report_button = tk.Button(self, text="Gerar relatório dos alunos", font=("TkDefaultFont", 12),
                                        command=self.request_report)
        request_report_button.pack(side="right", padx=(10, 20), pady=(20, 10))

                # botão de geração de relatório financeiro
        request_financial_report_button = tk.Button(self, text="Gerar relatório  FINANCEIRO dos alunos", font=("TkDefaultFont", 12),
                                        command=self.request_financial_report)
        request_financial_report_button.pack(side="right", padx=(50, 20), pady=(50, 10))

        # lista com os nomes, valores e planos comprados das compras feitas pelo sistema
        title_report_list = tk.Label(self, text="Relatório de usuários:", font=("TkDefaultFont", 14),
                                           anchor="w")
        title_report_list.pack(side="top", fill="x", pady=(40, 0))

        self.report_list = tk.Listbox(self, font=("TkDefaultFont", 12))
        self.report_list.pack(side="top", fill='x')


        financial_title_report_list = tk.Label(self, text="Relatório financeiro:", font=("TkDefaultFont", 14),
                                           anchor="w")
        financial_title_report_list.pack(side="bottom", fill="x", pady=(0, 400))

        self.financial_report_list = tk.Listbox(self, font=("TkDefaultFont", 12))
        self.financial_report_list.pack(side="bottom", fill='x', padx = (250))

    def request_report(self):
        list_users = self.controller.get_user_info()
        for user in list_users:
            self.report_list.insert("end", user.name)
            self.report_list.insert("end", user.treinos)
            self.report_list.insert("end", user.plans)
            self.report_list.insert("end", user.classes)
            self.report_list.insert("end", ' ')
            self.report_list.insert("end", ' ')
    
    def request_financial_report(self):
        total_aulas = []
        total_planos = []
        list_users = self.controller.get_user_info()
        self.financial_report_list.insert("end", 'PLANOS')
        for user in list_users:
            for plan in user.plans:
                self.financial_report_list.insert("end", f'R${plan.price}')
                total_planos.append(plan.price)

        self.financial_report_list.insert("end", f'Total planos: R${sum(total_planos)}')

        self.financial_report_list.insert("end", 'AULAS')
        for user in list_users:
            for aula in user.classes:
                self.financial_report_list.insert("end", f'R${aula.price}')
                total_aulas.append(aula.price)
        self.financial_report_list.insert("end", f'Total aulas: R${sum(total_aulas)}')
        self.financial_report_list.insert("end", '')

        self.financial_report_list.insert("end", f'TOTAL GANHO: R${sum(total_aulas) + sum(total_planos)}')

    def close_all(self):
        self.withdraw()
        self.master.quit()
        self.master.destroy()

class TrainerView(tk.Toplevel):
    def __init__(self, master, username):
        
        
        super().__init__(master)
        
        self.controller = TrainerController(self)
        
        self.geometry("1280x1280")
        self.title("INFit - Trainer")

        # nome do treinador direita em cima
        username_label = tk.Label(self, text=f"Olá treinador {username}", font=("TkDefaultFont", 12), anchor="e")
        username_label.pack(side="top", fill="x", pady=(10,0))

        # botão para sair
        quit_button = tk.Button(self, text="Logout", command=self.close_all, anchor="e")
        quit_button.pack(side="right", pady=(0,970))

        # lista com os planos/aulas que você já têm
        already_purchased_label = tk.Label(self, text="Usuários e informações:", font=("TkDefaultFont", 14), anchor="w")
        already_purchased_label.pack(side="top", fill="x", pady=(40,0))

        self.canvas = tk.Listbox(self, font=("TkDefaultFont", 12))
        self.canvas.pack(side="top", fill="x")

        # botão para criar treino
        create_train_button = tk.Button(self, text="Criar Treino", font=("TkDefaultFont", 12), command=self.create_train)
        create_train_button.pack(side="left", padx=(20,0), pady=(40,0))

        # botão para verificar treinos existentes
        check_existing_trains_button = tk.Button(self, text="Verificar Treinos Existentes", font=("TkDefaultFont", 12), command=self.get_trains)
        check_existing_trains_button.pack(side="left", padx=(20,0), pady=(10,0))

        # botão para verificar aulas existentes
        check_existing_trains_button = tk.Button(self, text="Verificar Aulas Existentes", font=("TkDefaultFont", 12), command=self.get_classes)
        check_existing_trains_button.pack(side="left", padx=(20,0), pady=(10,0))

        # botão para alterar os treinos dos usuários
        change_users_trains_button = tk.Button(self, text="Vincular treino à estudantes", font=("TkDefaultFont", 12), command=self.set_train_to_user)
        change_users_trains_button.pack(side="left", padx=(20,0), pady=(40,0))

        # botão para ver todos os estudantes
        get_students_button = tk.Button(self, text="Ver todos os estudantes", font=("TkDefaultFont", 12), command=self.get_all_students)
        get_students_button.pack(side="left", padx=(20,0), pady=(40,0))


        # botão para criar uma aula individual
        create_individual_class_button = tk.Button(self, text="Criar Aula Individual", font=("TkDefaultFont", 12), command=self.create_class)
        create_individual_class_button.pack(side="left", padx=(20,0), pady=(40,0))

    def get_trains(self):
        self.canvas.delete(0, 'end')

        for i in list_of_trains:
            self.canvas.insert('end', i)

    def get_classes(self):
        self.canvas.delete(0, 'end')

        for i in list_of_classes:
            self.canvas.insert('end', i)

    def get_all_students(self):
        self.canvas.delete(0, 'end')

        for i in list_of_students:
            self.canvas.insert('end', i.name)
    
    def create_train(self):
        amount = tk.simpledialog.askstring("CRIAR TREINO", "Digite o novo treino: ", parent = self)
        list_of_trains.append(Train(amount))
        self.get_trains()

    def create_class(self):
        name_Train = tk.simpledialog.askstring("CRIAR AULA INDIVIDUAL", "Digite a nova aula: ", parent = self)
        price_Train = tk.simpledialog.askstring("CRIAR AULA INDIVIDUAL", "Digite o preço: ", parent = self)
        date_Train = tk.simpledialog.askstring("CRIAR AULA INDIVIDUAL", "Digite a data: ", parent = self)
        list_of_classes.append(IndividualClass(name_Train, price_Train, date_Train))
        self.get_classes()

    def set_train_to_user(self):
        not_found_error = True

        name_Student = tk.simpledialog.askstring("Selecionar estudante", "Digite o nome do estudante: ", parent = self)
        for i in list_of_students:
            if i.name == name_Student:
                chosen_option = show_options(list_of_trains)
                i.treinos.append(chosen_option)
                not_found_error = False
                messagebox.showinfo("Treino registrado", f"O aluno {i.name} foi vinculado ao treino {chosen_option}!")

        if not_found_error:
            messagebox.showinfo("Aluno não existe", "O nome não se encontra na nossa database!")


    def close_all(self):
        self.withdraw()
        self.master.quit()
        self.master.destroy()

class OptionWindow:
    def __init__(self, options):
        self.options = options
        self.choice = None
        
        self.window = tk.Toplevel()
        self.window.title("Treinos disponíveis")
        
        self.label = tk.Label(self.window, text="Selecione um treino:")
        self.label.pack(padx=10, pady=10)
        
        self.buttons = []
        for option in options:
            button = tk.Button(self.window, text=option, command=lambda option=option: self.choose_option(option))
            button.pack(padx=10, pady=5)
            self.buttons.append(button)
    
    def choose_option(self, option):
        self.choice = option
        self.window.destroy()

def show_options(options):
    option_window = OptionWindow(options)
    option_window.window.wait_window()
    return option_window.choice


    




# Controller
class StudentController:
    def __init__(self, student, student_view):
        self.student = student
        self.student_view = student_view
    
    def update_balance(self, amount):
        return self.student.balance_add(amount)
    
    def get_student_balance(self):
        return self.student.get_balance()
    
    def purchase_plan(self, plan):
        return self.student.purchase_plan(plan)
        
    def purchase_class(self, indiv_class):
        return self.student.purchase_class(indiv_class)

    def get_classes_and_plans(self):
        with open('plans.bin', 'rb')  as f:
            list_of_plans = pickle.load(f)

        with open('classes.bin', 'rb')  as f:
            list_of_classes = pickle.load(f)

        all_options = deepcopy(list_of_plans)
        all_options.extend(list_of_classes)
        return all_options

    def edit_profile(self):
        pass
        while True:
            user_input = input("Digite o nome que deseja: ")
            if isinstance(user_input, str):
                self.student.name = user_input
                break
            print("Você não digitou um nome válido")

        while True:
            user_input = input("Digite o novo cpf (string): ")
            if isinstance(user_input, str):
                self.student.cpf = user_input
                break
            print("Você não digitou um nome válido")
        
        while True:
            user_input = input("Digite sua idade: ")

            try:
                user_input = int(user_input)
            except:
                pass

            if isinstance(user_input, int):
                self.student.age = user_input
                break
            print("Você não digitou uma idade válida")
        
    def show_student_info(self):
        self.student_view.display_student_info(self.student)


class TrainerController:
    def __init__(self, trainer_view):
        self.trainer_view = trainer_view

    def get_user_info(self):
        list_logins = []
        list_users = []
        with open('users.bin', 'rb+') as f:
            list_logins = pickle.load(f)

        for login in list_logins:
            list_users.append(login)

        return list_users


class ManagerController:
    def __init__(self, view):
        self.view = view

    def get_user_info(self):
        list_logins = []
        list_users = []
        with open('users.bin', 'rb+') as f:
            list_logins = pickle.load(f)

        for login in list_logins:
            list_users.append(login)

        return list_users


        



if __name__ == '__main__':
    # Define the filenames
    users_file = 'users.bin'
    trains_file = 'trains.bin'
    logins_file = 'logins.bin'
    plans_file = 'plans.bin'
    classes_file = 'classes.bin'

    if os.path.isfile(users_file) and os.path.isfile(trains_file) and os.path.isfile(logins_file) and os.path.isfile(plans_file) and os.path.isfile(classes_file):
        # Load the data from the files if they exist
        with open(users_file, 'rb') as f:
            list_of_students = pickle.load(f)
        with open(trains_file, 'rb') as f:
            list_of_trains = pickle.load(f)
        with open(logins_file, 'rb')  as f:
            users = pickle.load(f)
        with open(plans_file, 'rb')  as f:
            list_of_plans = pickle.load(f)
        with open(classes_file, 'rb')  as f:
            list_of_classes = pickle.load(f)

    else:
        users = []
        list_of_plans = []
        list_of_classes = []
        
        ##Instancio alguns logins de exemplo
        usernames = ['Artur', 'Arthur', 'Alberto', 'Anderson', 'Thiago']
        passwords = ['teste', 'teste','teste', 'teste','teste']
        login_types = ['user', 'user', 'trainer', 'trainer', 'manager']


        for i, x, y in zip(usernames, passwords, login_types):
            users.append(Login(i, x, y))

        list_of_plans.append(Plan("Anual", 1000))
        list_of_plans.append(Plan("Mensal", 150))
        list_of_plans.append(Plan("Semanal", 50))
        list_of_classes.append(IndividualClass('Aula de zumba', 80, '08/02/2023'))
        list_of_classes.append(IndividualClass('Aula de tango', 100, '09/02/2023'))
        list_of_classes.append(IndividualClass('Aula de MPB', 90, '09/02/2023'))

        list_of_trains = []
        list_of_trains.append(Train('Costas - Segunda exercícios 2-4-6-7, Pernas - Quarta exercícios 1-3-12-9, Braço/Peitoral - Sexta excercícios 12-41-3-17-33'))
        list_of_trains.append(Train('Costas - Segunda e Quarta exercícios 2-4-6-7, Pernas - Terça e Sábado exercícios 1-3-12-9, Braço/Peitoral - Quinta e Sexta excercícios 12-41-3-17-33'))

        list_of_students = []
        for x, login in enumerate(login_types):
            if login == 'user':
                list_of_students.append(Student(usernames[x], balance = x*100, cpf = None, age = 30-x*3, plans = [list_of_plans[x]], classes = [list_of_classes[x]], treinos = [Train(list_of_trains[x])]))

        with open('users.bin', 'wb') as f:
            pickle.dump(list_of_students, f)

        with open('trains.bin', 'wb') as f:
            pickle.dump(list_of_trains, f)

        with open('logins.bin', 'wb')  as f:
            pickle.dump(users, f)

        with open('plans.bin', 'wb')  as f:
            pickle.dump(list_of_plans, f)

        with open('classes.bin', 'wb')  as f:
            pickle.dump(list_of_classes, f)
    
    # Inicio pela tela de login e rodo o app.
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()

    with open('users.bin', 'wb') as f:
        pickle.dump(list_of_students, f)

    with open('logins.bin', 'wb')  as f:
        pickle.dump(users, f)

    with open('plans.bin', 'wb')  as f:
        pickle.dump(list_of_plans, f)

    with open('classes.bin', 'wb')  as f:
        pickle.dump(list_of_classes, f)

    with open('trains.bin', 'wb')  as f:
        pickle.dump(list_of_trains, f)

# %%


# %%



