import tkinter as tk
from tkinter import messagebox
import pickle
import csv
import os


class UrnaEletronica:
    def __init__(self, master):
        self.master = master
        self.master.title("Urna Eletrônica")
        self.master.geometry("400x500")
        self.master.resizable(False, False)

        # Dados
        self.candidatos = self.carregar_dados("candidatos.csv")
        self.eleitores = self.carregar_dados("eleitores.csv")
        self.votos = self.carregar_votos("votos.pkl")
        self.eleitor_atual = None

        # Interface inicial
        self.create_login_interface()

    def carregar_dados(self, arquivo):
        """Carrega os dados de eleitores ou candidatos de um arquivo CSV ou PKL."""
        if not os.path.exists(arquivo):
            messagebox.showerror("Erro", f"Arquivo {arquivo} não encontrado.")
            self.master.destroy()
            return {}

        if arquivo.endswith(".csv"):
            try:
                with open(arquivo, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    dados = {linha["id"]: linha["nome"] for linha in reader}
                    print(f"Dados carregados de {arquivo}: {dados}")  # Debug
                    return dados
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar {arquivo}: {str(e)}")
                self.master.destroy()
                return {}

    def carregar_votos(self, arquivo):
        """Carrega os votos armazenados ou cria uma nova estrutura."""
        if os.path.exists(arquivo):
            with open(arquivo, "rb") as f:
                return pickle.load(f)
        return {"branco": 0, "inválido": 0, **{nome: 0 for nome in self.candidatos.values()}}

    def salvar_votos(self, arquivo):
        """Salva os votos no arquivo .pkl."""
        with open(arquivo, "wb") as f:
            pickle.dump(self.votos, f)

    def create_login_interface(self):
        """Interface inicial para o login do eleitor."""
        self.clear_interface()

        tk.Label(self.master, text="Digite o título de eleitor", font=("Helvetica", 14)).pack(pady=10)
        self.titulo_entry = tk.Entry(self.master, font=("Helvetica", 16))
        self.titulo_entry.pack(pady=10)

        tk.Button(self.master, text="Confirmar", font=("Helvetica", 12), bg="green", fg="white", command=self.validar_eleitor).pack(pady=10)

    def validar_eleitor(self):
        """Valida o título de eleitor."""
        titulo = self.titulo_entry.get().strip()

        if titulo in self.eleitores:
            self.eleitor_atual = {"id": titulo, "nome": self.eleitores[titulo]}
            messagebox.showinfo("Eleitor Validado", f"Bem-vindo, {self.eleitor_atual['nome']}!")
            self.create_voto_interface()
        else:
            messagebox.showerror("Erro", "Título de eleitor inválido. Tente novamente.")

    def create_voto_interface(self):
        """Interface para o eleitor votar."""
        self.clear_interface()

        tk.Label(self.master, text=f"Eleitor: {self.eleitor_atual['nome']}", font=("Helvetica", 12)).pack(pady=5)
        tk.Label(self.master, text="Digite o número do candidato:", font=("Helvetica", 14)).pack(pady=10)

        self.numero_entry = tk.Entry(self.master, font=("Helvetica", 16))
        self.numero_entry.pack(pady=10)

        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Branco", font=("Helvetica", 12), bg="white", command=lambda: self.registrar_voto("branco")).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Confirmar", font=("Helvetica", 12), bg="green", fg="white", command=self.confirmar_voto).grid(row=0, column=1, padx=5)

        tk.Button(self.master, text="Corrige", font=("Helvetica", 12), bg="orange", fg="white", command=self.corrige).pack(pady=10)

    def confirmar_voto(self):
        """Confirma o voto digitado."""
        voto = self.numero_entry.get().strip()  # Obtém o número do candidato como string
        print(f"Voto digitado: {voto}, Candidatos disponíveis: {self.candidatos}")  # Debug
        if voto in self.candidatos:
            candidato = self.candidatos[voto]  # Mapeia o ID para o nome do candidato
            self.registrar_voto(candidato)
        else:
            self.registrar_voto("inválido")

    def registrar_voto(self, tipo):
        """Registra o voto (válido, branco ou inválido)."""
        if tipo in self.votos:
            self.votos[tipo] += 1
            messagebox.showinfo("Voto Computado", f"Você votou em: {tipo.capitalize() if tipo in ['branco', 'inválido'] else tipo}!")
            self.salvar_votos("votos.pkl")
            self.eleitor_atual = None
            self.create_login_interface()
        else:
            messagebox.showerror("Erro", "Voto inválido. Tente novamente.")

    def corrige(self):
        """Limpa o campo de voto."""
        self.numero_entry.delete(0, tk.END)

    def clear_interface(self):
        """Limpa os widgets da interface."""
        for widget in self.master.winfo_children():
            widget.destroy()

# Inicializando a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    urna = UrnaEletronica(root)
    root.mainloop()