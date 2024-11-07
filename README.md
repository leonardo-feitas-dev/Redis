### Estrutura do Banco de Dados Redis

1. **Sessão de Usuário (`session:{session_token}`)**
   - **Tipo**: `hash`
   - **Descrição**: Cada sessão ativa de usuário é armazenada com um conjunto de informações detalhadas, incluindo:
     - `user_id`: Identificador único do usuário.
     - `session_token`: Token único de autenticação da sessão.
     - `ip_address`: Endereço IP do usuário, útil para monitoramento e segurança.
     - `device_info`: Informações sobre o dispositivo usado pelo usuário.
     - `browser_info`: Dados sobre o navegador, também relevantes para segurança e análise.
     - `start_time`: Hora em que a sessão foi iniciada, no formato ISO 8601.
   - **Expiração**: A sessão é configurada para expirar após 2 horas, garantindo que sessões antigas sejam automaticamente removidas do banco de dados, o que otimiza o uso de memória e melhora a segurança ao finalizar sessões inativas.

2. **Cookies de Sessão (`cookie:session_token:{session_token}`)**
   - **Tipo**: `string`
   - **Descrição**: Armazena o valor do cookie associado ao token de sessão do usuário. Esse cookie permite que o sistema identifique o usuário em futuras visitas, mantendo a sessão ativa por um período prolongado.
   - **Expiração**: Configurada para 30 dias, permitindo que o usuário permaneça autenticado sem a necessidade de login frequente. Esse período também ajuda a gerenciar memória no Redis, eliminando cookies inativos automaticamente após um mês.

3. **Preferências de Usuário (`user:{user_id}:preferences`)**
   - **Tipo**: `hash`
   - **Descrição**: Cada usuário possui uma chave exclusiva de preferências, onde são armazenadas configurações pessoais como:
     - `language`: Idioma preferido pelo usuário, para personalização da interface.
     - `theme`: Tema visual (ex. claro ou escuro), proporcionando uma experiência de usuário adaptada.
     - `notifications`: Preferência sobre notificações (ativadas ou desativadas), armazenada em formato booleano (`true` ou `false`).
   - Essas preferências são recuperadas sempre que o usuário acessa o sistema, permitindo uma experiência personalizada de forma eficiente.

4. **Histórico de Navegação (`user:{user_id}:history`)**
   - **Tipo**: `list`
   - **Descrição**: Armazena o histórico de navegação de cada usuário, com detalhes sobre cada página visitada:
     - `page_visited`: URL ou nome da página visitada.
     - `visit_time`: Hora exata da visita, no formato ISO 8601.
     - `duration`: Duração da visita em segundos.
   - **Ordem**: Novos registros são adicionados no início da lista, tornando fácil acessar o histórico recente. Esse histórico permite análises de comportamento e melhora a experiência, recomendando ou destacando páginas com base no histórico anterior.

