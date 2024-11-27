from Database import Database

def main():
    db = Database("neo4j://localhost:7687", "neo4j", "password")

    while True:
        print("\n=== Rede Social ===")
        print("1. Criar Conta")
        print("2. Fazer Login")
        print("3. Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            login = input("Digite o login do usuário: ")
            senha = input("Digite a senha do usuário: ")
            db.criar_usuario(login, senha)
            print(f"Usuário {login} criado com sucesso!")

            # Menu de avaliação após a criação de conta
            while True:
                print("\n=== Menu de Avaliação ===")
                print("1. Avaliar Usuário")
                print("2. Sair da Conta")
                choice_avaliar = input("Escolha uma opção: ")

                if choice_avaliar == '1':
                    avaliado = input("Digite o login do avaliado: ")

                    if not db.usuario_existe(avaliado):
                        print(f"Usuário {avaliado} não encontrado.")
                        continue

                    try:
                        nota = float(input("Digite a nota (0 a 5): "))
                        if nota < 0 or nota > 5:
                            print("Nota deve estar entre 0 e 5.")
                            continue
                    except ValueError:
                        print("Por favor, insira um número válido para a nota.")
                        continue

                    contexto = input("Digite o contexto da avaliação: ")
                    db.avaliar_usuario(login, avaliado, nota, contexto)
                    print(f"{login} avaliou {avaliado} com a nota {nota} no contexto: '{contexto}'.")
                    
                elif choice_avaliar == '2':
                    print("Saindo da conta...")
                    break

                else:
                    print("Opção inválida. Tente novamente.")

        if choice == '2':
            login = input("Digite o login do usuário: ")
            senha = input("Digite a senha do usuário: ")

            if db.verificar_login(login, senha):
                print(f"Bem-vindo, {login}!")
            else:
                print("Usuário ou senha incorretos.")
                criar = input("Deseja criar uma nova conta? (s/n): ").strip().lower()
                if criar == 's':
                    db.criar_usuario(login, senha)
                    print(f"Usuário {login} criado com sucesso!")
                else:
                    print("Retornando ao menu principal.")
                    continue

            # Menu de avaliação após login ou criação de conta
            while True:
                print("\n=== Menu de Avaliação ===")
                print("1. Avaliar Usuário")
                print("2. Sair da Conta")
                choice_avaliar = input("Escolha uma opção: ")

                if choice_avaliar == '1':
                    avaliado = input("Digite o login do avaliado: ")

                    if not db.usuario_existe(avaliado):
                        print(f"Usuário {avaliado} não encontrado.")
                        continue

                    try:
                        nota = float(input("Digite a nota (0 a 5): "))
                        if nota < 0 or nota > 5:
                            print("Nota deve estar entre 0 e 5.")
                            continue
                    except ValueError:
                        print("Por favor, insira um número válido para a nota.")
                        continue

                    contexto = input("Digite o contexto da avaliação: ")
                    db.avaliar_usuario(login, avaliado, nota, contexto)
                    print(f"{login} avaliou {avaliado} com a nota {nota} no contexto: '{contexto}'.")

                elif choice_avaliar == '2':
                    print("Saindo da conta...")
                    break

                else:
                    print("Opção inválida. Tente novamente.")

        elif choice == '3':
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

    db.close()


if __name__ == "__main__":
    main()
