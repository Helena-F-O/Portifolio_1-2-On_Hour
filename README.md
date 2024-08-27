# Portifolio 1 e 2 
## Projeto On Hour

### Resumo
   O projeto "On Hour" propõe a implementação de uma plataforma para o controle de horas complementares dos alunos da faculdade. Este sistema permitirá aos alunos criar perfis individuais, registrar horas referentes a atividades extracurriculares e associar os certificados correspondentes. Além disso, a plataforma oferecerá um painel de controle intuitivo, facilitando a visualização das horas acumuladas. Os usuários também poderão gerar arquivos para impressão e validação pelo coordenador, proporcionando uma gestão eficiente das horas complementares.


1. Introdução
   
   O projeto "On Hour" surge da necessidade de melhorar e simplificar o controle das horas complementares dos alunos da faculdade. O processo atual, sendo manual e sujeito a erros, demanda uma solução mais eficiente.
   A relevância deste projeto na engenharia de software está na aplicação prática de conceitos para desenvolver uma solução que melhora a eficiência administrativa e a experiência dos alunos. A automação do registro e controle das horas complementares reduzirá a carga burocrática e aumentará a precisão e transparência do processo.
   O objetivo principal do projeto "On Hour" é criar uma plataforma robusta e intuitiva para o controle de horas complementares, oferecendo aos alunos uma ferramenta eficaz para o gerenciamento de suas atividades extracurriculares. Além disso, objetiva-se proporcionar ao corpo docente e coordenadores um meio eficiente para validar e acompanhar o progresso dos alunos. É um projeto escalável para conexão com outros sistemas via APIs. 
   Objetivos secundários incluem a promoção da colaboração entre alunos e facilitação do processo de emissão de certificados, contribuindo para uma experiência acadêmica mais fluida e transparente.


2. Descrição do Projeto

   O tema central do projeto "On Hour" é a concepção e implementação de uma plataforma online dedicada ao controle de horas complementares dos alunos. O produto resultante será uma ferramenta acessível e intuitiva que permitirá aos usuários gerenciar eficientemente suas atividades extracurriculares, registrando horas e associando certificados de forma organizada. Além disso, haverá a possibilidade de conectar com os sistemas da instituição via uma API, onde já possui uma rota pronta para isso. Adicionalmente, será disponibilizada uma rota onde é possível que a instituição consiga acessar o relatório de horas de um aluno através do CPF dele.
	Para tanto desejo resolver os seguintes problemas:
   Gestão Manual Desafiadora: A abordagem manual atual para o controle de horas complementares é propensa a erros e demanda esforço significativo. O projeto visa resolver esse problema automatizando o processo, proporcionando uma solução mais precisa e eficiente.
   Falta de Transparência: A ausência de uma plataforma dedicada para o registro de horas pode resultar em falta de transparência para os alunos e coordenadores. O "On Hour" busca resolver esse problema, oferecendo uma interface clara e acessível para visualização e validação das horas acumuladas.
   Dificuldade na Emissão de Certificados: A atual complexidade na emissão de certificados para atividades complementares pode ser simplificada. O projeto aborda essa questão, facilitando a associação de certificados às atividades registradas e oferecendo a geração simplificada de arquivos para validação.
   As limitações encontradas para o software são as seguintes:
Integração com Outros Sistemas: O projeto "On Hour" não incluirá a integração completa com outros sistemas acadêmicos. A plataforma se concentrará exclusivamente no controle de horas complementares, não abordando a integração total com outros aspectos da gestão acadêmica.
   Validação de Conteúdo dos Certificados: A validação de conteúdo específico dos certificados associados às atividades registradas não será abordada integralmente pelo projeto. A responsabilidade pela verificação do conteúdo permanecerá com os coordenadores acadêmicos.
   Personalização Extensiva dos Perfis: Embora a plataforma permita aos alunos criar e gerenciar perfis, as opções de personalização extensiva desses perfis não serão uma prioridade. O foco estará na funcionalidade central do controle de horas complementares.




3. Especificação Técnica
   Neste tópico irei fazer uma descrição detalhada da proposta, incluindo requisitos de software, protocolos, algoritmos, procedimentos, formatos de dados, etc.


	3.1. Requisitos de Software
	
	
	Requisitos Funcionais
	
	Login
	
	RF01: O sistema deve permitir que os usuários realizem login.
	
	RF02: O sistema deve exibir um alerta de login incorreto quando as credenciais inseridas não forem válidas.
	
	RF03: O sistema deve exibir um alerta de login fora do padrão quando as credenciais não seguirem o formato esperado.
	
	
	Gerenciamento de Usuários
	
	RF04: O sistema deve permitir que os usuários criem novas contas.
	
	RF05: O sistema deve permitir que os usuários visualizem suas informações.
	
	RF06: O sistema deve permitir que os usuários editem suas informações.
	
	RF07: O sistema deve permitir que os usuários excluam suas contas.
	
	RF08: O sistema deve permitir que os usuários realizem logout.
	
	
	Dashboard
	
	RF09: O sistema deve fornecer uma visualização das horas complementares dos alunos.
	
	RF10: O sistema deve permitir o acesso aos certificados dos alunos.
	
	
	Gerenciamento de Certificados
	
	RF11: O sistema deve permitir que os usuários consultem certificados.
	
	RF12: O sistema deve permitir que os usuários adicionem novos certificados.
	
	RF13: O sistema deve permitir que os usuários editem certificados existentes.
	
	RF14: O sistema deve permitir que os usuários excluam certificados.
	
	RF15: O sistema deve permitir a geração de um PDF dos certificados para conferência com o coordenador.
	
	
	Relatórios de Horas
	
	RF16: O sistema deve permitir a geração de relatórios de horas complementares.
	
	RF17: O sistema deve permitir que os usuários salvem relatórios de horas.
	
	RF18: O sistema deve permitir que os usuários visualizem relatórios de horas.
	
	RF19: O sistema deve permitir o acesso aos relatórios de horas por rota específica.
	
	RF20: O sistema deve permitir a consulta de relatórios de horas de um aluno específico pelo CPF.
	
	RF21: O sistema deve permitir a exportação de relatórios de horas para PDF.
	
	
	
	Requisitos Não Funcionais (RNF)
	
	Segurança
	
	RNF01: O sistema deve garantir que o acesso ao relatório de horas seja protegido por autenticação e autorização de usuários. 
	
	RNF02: O sistema deve implementar medidas de proteção contra ataques como injeção de SQL, XSS (Cross-Site Scripting), CSRF (Cross-Site Request Forgery) e outros ataques comuns na web, também para a rota de acesso ao relatório de horas. 
	
	RNF03: O sistema deve criptografar os dados sensíveis presentes nos relatórios de horas, como informações pessoais dos alunos.
	
	
	Disponibilidade
	
	RNF04: O sistema deve assegurar que a rota de acesso ao relatório de horas esteja disponível de forma contínua, implementando estratégias de backup e recuperação de dados em caso de falha. 
	
	RNF05: O sistema deve garantir tolerância a falhas na rota de acesso ao relatório de horas para que a aplicação permaneça funcional mesmo em situações adversas.
	
	
	Usabilidade
	
	RNF06: O sistema deve certificar-se de que a interface de usuário para visualização e interação com o relatório de horas seja intuitiva e fácil de usar. 
	
	RNF07: O sistema deve garantir consistência na interface de usuário entre o restante do sistema e a rota de acesso ao relatório de horas. 
	
	RNF08: O sistema deve adaptar a responsividade da interface de usuário para diferentes dispositivos e tamanhos de tela, incluindo a visualização do relatório de horas em dispositivos móveis.
	
	
	Manutenibilidade
	
	RNF09: O sistema deve manter clareza e legibilidade do código relacionado à implementação da rota de acesso ao relatório de horas. 
	
	RNF10: O sistema deve facilitar a extensão e manutenção do sistema, incluindo a possibilidade de adicionar novas funcionalidades ou fazer ajustes na rota de acesso ao relatório de horas de forma eficiente. 
	
	RNF11: O sistema deve documentar adequadamente o código-fonte e a arquitetura relacionados à rota de acesso ao relatório de horas, para facilitar futuras manutenções e atualizações.
	
	
	
	Representação dos Requisitos: Aqui irei representar os RFs por meio de um Diagrama de Casos de Uso (UML).
	Endereço online: https://lucid.app/lucidchart/d45b7912-de57-4c6f-9e55-31604ccb2ea2/edit?viewport_loc=-1919%2C-101%2C2219%2C1076%2C0_0&invitationId=inv_1c4e6fdf-facf-494d-b951-f84a9f0fbb27
	Figura 1 - Diagrama UML


	3.2. Considerações de Design
   	Durante a concepção do projeto "On Hour", diversas alternativas de design foram consideradas para atender aos requisitos funcionais e não funcionais estabelecidos. Neste contexto teremos as definições da arquitetura neste tópico.
   	Foi adotada uma arquitetura de aplicação web baseada no padrão MVC (Model-View-Controller) devido à sua capacidade de separar claramente as responsabilidades entre a lógica de negócios, a apresentação e a manipulação de dados. Isso permite uma maior modularidade e facilita a manutenção do código ao longo do tempo.
   	Para garantir a escalabilidade e a flexibilidade do sistema, optei por implementar o projeto usando uma arquitetura de microservices. Cada serviço é responsável por uma função específica, como autenticação de usuários, gestão de horas complementares e geração de PDFs, facilitando a evolução independente de cada componente e permitindo uma fácil integração com sistemas externos no futuro.
   	Para atender aos requisitos de desempenho, segurança e usabilidade, optei por utilizar tecnologias comprovadas e amplamente adotadas pela comunidade de desenvolvimento web. Isso inclui o uso de HTML, CSS e JavaScript para o frontend, Python para o backend e MySQL como banco de dados relacional.
   	Dada a importância da segurança dos dados dos usuários, irei implementar várias camadas de segurança no sistema. Isso inclui autenticação e autorização robustas usando tokens JWT (JSON Web Tokens), criptografia de dados sensíveis no banco de dados e prevenção contra ataques comuns na web, como injeção de SQL e XSS.
   	A arquitetura do projeto "On Hour" é composta por diversos componentes interconectados, cada um desempenhando um papel específico no funcionamento do sistema. Abaixo estão os principais componentes e suas interconexões:
	   
	Frontend (Cliente Web):
	   - Responsável pela interface do usuário, interação e apresentação dos dados.
	   - Desenvolvido usando HTML, CSS e JavaScript para criar uma experiência de usuário moderna e responsiva.
	
	Backend (Servidor):
	   - Gerencia a lógica de negócios, autenticação de usuários, gestão de horas complementares e geração de PDFs.
	   - Desenvolvido usando Python, fornecendo uma base sólida e eficiente para o desenvolvimento de aplicativos web.
	
	Banco de Dados:
	   - Armazena todos os dados do sistema, incluindo informações de usuários, registros de horas complementares e certificados associados.
	   - Utiliza MySQL como banco de dados relacional devido à sua confiabilidade e suporte à escalabilidade.
	
	Interconexões:
	   - O Frontend se comunica com o Backend através de APIs RESTful, enviando solicitações HTTP para recuperar e enviar dados.
	   - O Backend acessa o Banco de Dados para recuperar e armazenar informações relevantes, garantindo a persistência dos dados do sistema.
	   - A autenticação de usuários é gerenciada pelo Backend, que emite tokens JWT para permitir o acesso seguro aos recursos protegidos.
	
	
	A arquitetura do projeto "On Hour" adere aos seguintes padrões de arquitetura:
	
	MVC (Model-View-Controller): Organização das responsabilidades em modelos, visões e controladores para uma separação clara de preocupações e uma estrutura de código mais modular.
	Microserviços: Implementação de serviços independentes e especializados, facilitando a escalabilidade, manutenção e evolução do sistema.
	
	Modelos C4
	   A arquitetura do projeto "On Hour" pode ser detalhada usando os modelos C4 (Context, Containers, Components, Code). Abaixo estão os principais aspectos de cada modelo:

   	Contexto:
	   O contexto do sistema "On Hour" é uma plataforma online dedicada ao controle de horas complementares dos alunos, oferecendo uma solução acessível e intuitiva para gerenciar eficientemente atividades extracurriculares e associar certificados de forma organizada.
	   
	Contêineres:
	   Os principais contêineres do sistema incluem:
	   Cliente Web (Frontend)
	   Servidor (Backend)
	   Banco de Dados
	   
	Componentes:
	   Os principais componentes incluem:
	   Autenticação de Usuários
	   Gestão de Horas Complementares
	   Associação de Certificados
	   Geração de PDFs
	   
	Código:
	   O código-fonte do sistema é desenvolvido usando tecnologias modernas e práticas de programação, seguindo as melhores práticas de desenvolvimento de software e padrões de codificação.
	   

	3.3. Stack Tecnológica
	
	Linguagens de Programação:
	HTML, CSS e JavaScript: Escolhi essas linguagens para o desenvolvimento do frontend devido à sua ampla compatibilidade com navegadores web e sua capacidade de criar interfaces de usuário interativas e responsivas.
	Python: Optei por Python para o desenvolvimento do backend devido à sua simplicidade, legibilidade e ampla gama de bibliotecas disponíveis. Python é uma escolha popular para o desenvolvimento web devido à sua eficiência no processamento de solicitações HTTP e na manipulação de dados.
	SQL (MySQL): Utilizarei SQL para interagir com o banco de dados MySQL, pois é uma linguagem padrão para consultas e manipulações de dados em bancos de dados relacionais.
	   
	Frameworks e Bibliotecas:
	jQuery: Utilizarei o jQuery para o desenvolvimento do frontend devido à sua capacidade de simplificar a manipulação do DOM, facilitando o desenvolvimento de interfaces de usuário interativas e a manipulação de eventos.
	Spring Boot: Optei por Spring Boot para o desenvolvimento do backend devido à sua facilidade de configuração, suporte à criação de APIs RESTful e integração com o ecossistema Spring, proporcionando uma base sólida para o desenvolvimento de aplicativos Java.
	JWT (JSON Web Tokens): Para autenticação de usuários, farei o uso de tokens JWT devido à sua facilidade de implementação, capacidade de transferir informações de forma segura entre partes e suporte a autenticação stateless.
	   
	Ferramentas de Desenvolvimento e Gestão de Projeto:
	Visual Studio Code: Utilizarei o Visual Studio Code como ambiente de desenvolvimento principal devido à sua leveza, extensibilidade e suporte integrado para diversas linguagens de programação.
	Git e GitHub: Farei uso do Git como sistema de controle de versão e GitHub como plataforma para hospedagem de código-fonte, facilitando o trabalho colaborativo e o gerenciamento de mudanças no código.
	Trello: Para gestão de projeto, adotarei o Trello devido à sua simplicidade e flexibilidade na organização de tarefas, permitindo o acompanhamento do progresso do projeto de forma clara e eficiente.
	   
	Diagrama de Componentes:
	Um diagrama de componentes detalhando a interação entre os componentes frontend (Cliente Web), backend (Servidor) e banco de dados será elaborado para fornecer uma visão clara da estrutura do sistema e das dependências entre os diferentes componentes.
	
	
	
	
	3.4. Considerações de Segurança
	Análise de Possíveis Questões de Segurança:
	Autenticação e Autorização: Será implementado um sistema robusto de autenticação e autorização para garantir que apenas usuários autorizados tenham acesso aos recursos protegidos da aplicação.
   	Proteção contra Injeção de SQL: Utilizarei consultas parametrizadas e validação de entrada para mitigar o risco de ataques de injeção de SQL, garantindo que os dados inseridos no banco de dados sejam seguros.
	   
	Prevenção contra XSS (Cross-Site Scripting): 
	Farei uso de técnicas como sanitização de entrada e saída de dados para prevenir ataques de XSS, protegendo os usuários contra a execução de scripts maliciosos em seus navegadores.
	Validação de Dados de Entrada: Será implementado validações de entrada em todas as formas de dados enviados pelos usuários para garantir que apenas dados válidos e seguros sejam processados pela aplicação.
	   
	Criptografia de Dados Sensíveis: 
	Utilizarei algoritmos de criptografia para proteger dados sensíveis, como senhas e informações pessoais dos usuários, armazenando-os de forma segura no banco de dados.
	Auditoria e Monitoramento: Implementarem os registros de auditoria e monitoramento em tempo real para detectar e responder rapidamente a quaisquer atividades suspeitas ou tentativas de violação de segurança.
	
	
4. Cronograma
	Refinamento do Documento RFC (Request for Comments)
	O primeiro passo do cronograma é o refinamento do documento RFC (Request for Comments), uma revisão cuidadosa do documento RFC, garantindo clareza, completude e consistência nas informações apresentadas. Correção de possíveis erros gramaticais, ortográficos ou de formatação, além da incorporação de feedbacks de colegas, orientadores e profissionais experientes na área, visando melhorar a qualidade do documento.
	   
	Preparação para a Banca de Defesa do Tema
	Após isso a preparação para a Banca de Defesa do Tema, elaboração de uma apresentação concisa e persuasiva que destaque os principais pontos do projeto, objetivos, metodologia, resultados esperados e benefícios. Prática de apresentação oral, visando aprimorar habilidades de comunicação e garantir uma apresentação clara e envolvente durante a banca e também a revisão aprofundada do conteúdo do documento RFC e familiarização com os detalhes do projeto, garantindo domínio sobre o tema para responder a possíveis questionamentos dos avaliadores.
	   
	Desenvolvimento do Projeto "On Hour"
	O desenvolvimento do projeto "On Hour" envolve a implementação das funcionalidades especificadas no documento RFC, seguindo as melhores práticas de desenvolvimento de software e utilizando as tecnologias e ferramentas definidas. Durante este processo, são realizados testes rigorosos para garantir a qualidade e confiabilidade do sistema, incluindo testes de unidade, integração e aceitação. Além disso, interações frequentes com os usuários finais e feedback contínuo são essenciais para realizar ajustes e melhorias ao longo do desenvolvimento.
	   
	Preparação para a Banca de Defesa do Projeto
	A preparação para a banca de defesa do projeto inclui a demonstração do sistema "On Hour" em funcionamento, destacando as principais funcionalidades, interface do usuário e fluxos de trabalho. Também envolve a preparação de uma apresentação detalhada sobre o processo de desenvolvimento, abordando desafios enfrentados, soluções implementadas e lições aprendidas. É importante antecipar possíveis perguntas dos avaliadores e preparar respostas claras e fundamentadas. Além disso, uma revisão final do código-fonte, documentação e artefatos do projeto é realizada para garantir coesão e consistência.
	   
	Participação na Banca de Defesa do Projeto
	Durante a participação na banca de defesa do projeto, o objetivo é apresentar o "On Hour" aos avaliadores, demonstrando conhecimento técnico, capacidade de análise e tomada de decisão. As perguntas e críticas dos avaliadores devem ser respondidas de forma objetiva e confiante, evidenciando domínio sobre o projeto e suas nuances. É importante aceitar feedbacks construtivos e mostrar disposição para discutir possíveis melhorias ou áreas de aprimoramento do projeto.
	   
6. Referências
	Documentação Oficial e Guias Online
	Documentação das Linguagens de Programação e Tecnologias: 
	Python: https://docs.python.org/3/ 
	HTML: https://developer.mozilla.org/en-US/docs/Web/HTML 
	CSS: https://developer.mozilla.org/en-US/docs/Web/CSS 
	Bootstrap: https://getbootstrap.com.br/docs/4.1/getting-started/introduction/ 
	Tutoriais e Guias Online: 
	MDN Web Docs: https://developer.mozilla.org/en-US/ 
	W3Schools: https://www.w3schools.com/ 
	Stack Overflow: https://stackoverflow.com/ 
	Frameworks e Bibliotecas
	jQuery: "jQuery: The Write Less, Do More, JavaScript Library." jQuery Foundation. https://jquery.com
	Spring Boot: "Spring Boot Reference Documentation." Pivotal Software. https://spring.io/projects/spring-boot
	JWT (JSON Web Tokens): "Introduction to JSON Web Tokens." Auth0. https://jwt.io/introduction
	Bootstrap: "Bootstrap: The most popular HTML, CSS, and JS library in the world." Bootstrap Team. https://getbootstrap.com
	Ferramentas de Desenvolvimento e Gestão de Projetos
	Visual Studio Code: "Visual Studio Code Documentation." Microsoft. https://code.visualstudio.com/docs
	Git: "Git Documentation." Software Freedom Conservancy. https://git-scm.com/doc
	GitHub: "GitHub Guides." GitHub. https://guides.github.com
	Trello: "Getting Started with Trello." Atlassian. https://trello.com/en-US/guide
	
	
	Outras Ferramentas
	MySQL Workbench: "MySQL Workbench Manual." Oracle Corporation. https://dev.mysql.com/doc/workbench/en/
	Lucidchart: "Lucidchart Documentation." Lucid Software. https://www.lucidchart.com/pages/how-to
	Postman: "Postman Learning Center." Postman. https://learning.postman.com
	OWASP Zap: "OWASP ZAP: Zed Attack Proxy." OWASP Foundation. https://www.zaproxy.org
	
	
	6. Apêndices
	Diagrama de Fluxo de Dados
	
	![image](https://github.com/user-attachments/assets/7ae78147-dafc-47bb-b5ae-fce3b32f6e0e)
	
	Figura 2 - Diagrama Fluxo de Dados
	
	
	Fluxograma do processo
	Diagrama de classe do projeto
	
	![image](https://github.com/user-attachments/assets/7e3e5fc7-c688-4082-8c93-67d2709c4957)
	
	Figura 2 - Diagrama de Classe
	
	
	Fluxograma do Projeto
	
	![image](https://github.com/user-attachments/assets/8bd75233-51b0-48ef-8c6e-e2632f9f88e5)
	
	Figura 3 - Fluxograma Do Projeto Parte 1
	
	![image](https://github.com/user-attachments/assets/a70e0184-098e-456b-88c9-66d2936643ae)
	
	Figura 4 - Fluxograma Do Projeto Parte 2
	
	![image](https://github.com/user-attachments/assets/22e35c80-4622-407d-b34d-ae97262fa2b0)
	
	Figura 5 - Fluxograma Do Projeto Parte 3
	
	
	Casos de Uso:
	Caso de Uso 1: Login no Sistema
	Ator: Usuário
	Fluxo Principal:
	O usuário acessa o sistema.
	O usuário insere seu nome de usuário e senha.
	O usuário clica no botão "Login".
	O sistema valida as credenciais do usuário.
	O sistema exibe a tela inicial após o login bem-sucedido.
	Fluxos Alternativos:
	A1: Credenciais incorretas.
	O sistema exibe uma mensagem de alerta de login incorreto.
	
	
	A2: Formato de credenciais fora do padrão.
	O sistema exibe uma mensagem de alerta de login fora do padrão.
	
	
	Caso de Uso 2: Logout do Sistema
	Ator: Usuário
	Fluxo Principal:
	O usuário clica no botão "Logout".
	O sistema encerra a sessão do usuário.
	O sistema redireciona o usuário para a página de login.
	
	
	Caso de Uso 3: Visualizar Horas Complementares
	Ator: Usuário
	Fluxo Principal:
	O usuário acessa o sistema e faz login.
	O usuário navega até a seção "Dash".
	O sistema exibe as horas complementares acumuladas pelo usuário.
	
	
	Caso de Uso 4: Consultar Certificados
	Ator: Usuário
	Fluxo Principal:
	O usuário acessa o sistema e faz login.
	O usuário navega até a seção "Certificados".
	O usuário seleciona a opção para consultar certificados.
	O sistema exibe a lista de certificados registrados.
	
	
	Caso de Uso 5: Adicionar Certificado
	Ator: Usuário
	Fluxo Principal:
	O usuário acessa o sistema e faz login.
	O usuário navega até a seção "Certificados".
	O usuário seleciona a opção para adicionar um novo certificado.
	O usuário preenche as informações do certificado.
	O usuário confirma a adição do certificado.
	O sistema registra o novo certificado e o exibe na lista de certificados.
	
	
	Caso de Uso 6: Editar Certificado
	Ator: Usuário
	Fluxo Principal:
	
	
	O usuário acessa o sistema e faz login.
	O usuário navega até a seção "Certificados".
	O usuário seleciona um certificado existente para editar.
	O usuário modifica as informações do certificado.
	O usuário confirma as alterações.
	O sistema atualiza o certificado com as novas informações.
	
	
	Caso de Uso 7: Excluir Certificado
	Ator: Usuário
	Fluxo Principal:
	O usuário acessa o sistema e faz login.
	O usuário navega até a seção "Certificados".
	O usuário seleciona um certificado existente para excluir.
	O usuário confirma a exclusão.
	O sistema remove o certificado da lista.
	
	
	Caso de Uso 8: Gerar PDF para Conferência com o Coordenador
	Ator: Usuário
	Fluxo Principal:
	O usuário acessa o sistema e faz login.
	O usuário navega até a seção "Certificados".
	O usuário seleciona a opção para gerar um PDF de conferência.
	O sistema gera o PDF com os certificados selecionados.
	O usuário visualiza e salva o PDF gerado.
	
	
	Caso de Uso 9: Consultar Relatório de Horas de um Aluno pelo CPF
	Ator: Administrador / Coordenador
	Fluxo Principal:
	O administrador/coordenador acessa o sistema e faz login.
	O administrador/coordenador navega até a seção de consulta de relatórios.
	O administrador/coordenador insere o CPF do aluno.
	O administrador/coordenador solicita a consulta.
	O sistema exibe o relatório de horas do aluno.
	
	
	Caso de Uso 10: Visualizar Relatório de Horas
	Ator: Administrador / Coordenador
	Fluxo Principal:
	O administrador/coordenador acessa o sistema e faz login.
	O administrador/coordenador navega até a seção de consulta de relatórios.
	O administrador/coordenador seleciona um relatório de horas.
	O sistema exibe o relatório de horas do aluno.
	
	
	Caso de Uso 11: Exportar Relatório de Horas para PDF
	Ator: Administrador / Coordenador
	Fluxo Principal:
	O administrador/coordenador acessa o sistema e faz login.
	O administrador/coordenador navega até a seção de consulta de relatórios.
	O administrador/coordenador seleciona um relatório de horas.
	O administrador/coordenador escolhe a opção para exportar para PDF.
	O sistema gera e salva o relatório de horas em formato PDF.
	
	
	## GitHub Pages (visualização do Projeto)
	
	https://helena-f-o.github.io/Portifolio_1-2-On_Hour/
