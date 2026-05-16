from medalert.services import add_medication, validate_time_format, mark_as_taken, remove_medication
from medalert.storage import load_data, save_data
from medalert.api import fetch_drug_info, format_drug_info


def menu():
    print("\n=== MedAlert CLI ===")
    print("1 - Adicionar medicamento")
    print("2 - Listar medicamentos")
    print("3 - Marcar como tomado")
    print("4 - Remover medicamento")
    print("5 - Consultar medicamento na API (OpenFDA)")
    print("0 - Sair")


def main():
    medications = load_data()

    while True:
        menu()
        choice = input("Escolha uma opção: ").strip()

        if choice == "1":
            name = input("Nome do medicamento: ").strip()
            dosage = input("Dosagem (ex: 500mg): ").strip()
            time = input("Horário (HH:MM): ").strip()

            if not validate_time_format(time):
                print("Horário inválido! Use o formato HH:MM.")
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
                print("\n=== Lista de Medicamentos ===")
                for i, med in enumerate(medications, start=1):
                    status = "Tomado" if med.taken else "Pendente"
                    print(f"{i} - {med.name} ({med.dosage}) às {med.time} [{status}]")

        elif choice == "3":
            try:
                index = int(input("Número do medicamento: "))
                mark_as_taken(medications, index)
                save_data(medications)
                print("Medicamento marcado como tomado!")
            except ValueError:
                print("Erro: índice inválido.")

        elif choice == "4":
            try:
                index = int(input("Número do medicamento: "))
                remove_medication(medications, index)
                save_data(medications)
                print("Medicamento removido!")
            except ValueError:
                print("Erro: índice inválido.")

        elif choice == "5":
            drug_name = input("Digite o nome do medicamento para consulta: ").strip()

            try:
                info = fetch_drug_info(drug_name)
                print(format_drug_info(info))
            except Exception as e:
                print(f"Erro ao consultar API: {e}")

        elif choice == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()
