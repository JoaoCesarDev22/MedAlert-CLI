from medalert.services import add_medication, validate_time_format, mark_as_taken
from medalert.storage import load_data, save_data

#so-para-atualizar
def menu():
    print("\n=== MedAlert CLI ===")
    print("1 - Adicionar medicamento")
    print("2 - Listar medicamentos")
    print("3 - Marcar como tomado")
    print("4 - Remover medicamento")
    print("0 - Sair")


def main():
    medications = load_data()

    while True:
        menu()
        choice = input("Escolha uma opção: ")

        if choice == "1":
            name = input("Nome do medicamento: ")
            dosage = input("Dosagem (ex: 500mg): ")
            time = input("Horário (HH:MM): ")

            if not validate_time_format(time):
                print("Horário inválido!")
                continue

            try:
                add_medication(medications, name, dosage, time)
                save_data(medications)
                print("Medicamento adicionado com sucesso!")
            except ValueError as e:
                print(f"Erro: {e}")

        elif choice == "2":
            if not medications:
                print("Nenhum medicamento cadastrado.")
            else:
                for i, med in enumerate(medications):
                    status = "Tomado" if med.taken else "Pendente"
                    print(f"{i} - {med.name} ({med.dosage}) às {med.time} [{status}]")

        elif choice == "3":
            try:
                index = int(input("Índice do medicamento: "))
                mark_as_taken(medications, index)
                save_data(medications)
                print("Medicamento marcado como tomado!")
            except (ValueError, IndexError):
                print("Índice inválido!")

        elif choice == "4":
            try:
                index = int(input("Índice do medicamento: "))
                medications.pop(index)
                save_data(medications)
                print("Medicamento removido!")
            except (ValueError, IndexError):
                print("Índice inválido!")

        elif choice == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()