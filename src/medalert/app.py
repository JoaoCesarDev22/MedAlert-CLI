from medalert.services import validate_time_format
from medalert.db_services import (
    add_medication_db,
    list_medications_db,
    mark_as_taken_db,
    remove_medication_db,
)
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
    while True:
        menu()
        choice = input("Escolha uma opção: ").strip()

        if choice == "1":
            name = input("Nome do medicamento: ").strip()
            dosage = input("Dosagem (ex: 500mg): ").strip()
            time = input("Horário (HH:MM): ").strip()

            if not name:
                print("Erro: Nome do medicamento não pode ser vazio.")
                continue
            if not dosage:
                print("Erro: Dosagem não pode ser vazia.")
                continue
            if not validate_time_format(time):
                print("Horário inválido! Use o formato HH:MM.")
                continue

            try:
                new_id = add_medication_db(name, dosage, time)
                print(f"Medicamento adicionado com sucesso! (ID: {new_id})")
            except Exception as e:
                print(f"Erro ao adicionar: {e}")

        elif choice == "2":
            try:
                medications = list_medications_db()
            except Exception as e:
                print(f"Erro ao listar: {e}")
                continue

            if not medications:
                print("Nenhum medicamento cadastrado.")
            else:
                print("\n=== Lista de Medicamentos ===")
                for med in medications:
                    status = "Tomado" if med["tomado"] else "Pendente"
                    print(
                        f"{med['id']} - {med['nome']} ({med['dosagem']}) "
                        f"às {med['horario']} [{status}]"
                    )

        elif choice == "3":
            try:
                med_id = int(input("ID do medicamento: ").strip())
            except ValueError:
                print("Erro: ID inválido.")
                continue

            try:
                if mark_as_taken_db(med_id):
                    print("Medicamento marcado como tomado!")
                else:
                    print("Nenhum medicamento encontrado com esse ID.")
            except Exception as e:
                print(f"Erro ao atualizar: {e}")

        elif choice == "4":
            try:
                med_id = int(input("ID do medicamento: ").strip())
            except ValueError:
                print("Erro: ID inválido.")
                continue

            try:
                if remove_medication_db(med_id):
                    print("Medicamento removido!")
                else:
                    print("Nenhum medicamento encontrado com esse ID.")
            except Exception as e:
                print(f"Erro ao remover: {e}")

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
