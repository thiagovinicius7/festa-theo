// Textos editáveis do convite (o painel usa esta lista para montar o formulário).
// Em "padrao", {total} é trocado pela quantidade de pessoas confirmadas.
export const TEXTOS = [
  // Topo
  { g: 'Topo', k: 'faixa', rot: 'Faixa vermelha', padrao: 'VOCÊ FOI CONVOCADO' },
  { g: 'Topo', k: 'av', rot: 'Palavra acima do nome', padrao: 'AVATAR' },
  { g: 'Topo', k: 'nm', rot: 'Nome grande', padrao: 'Theo' },
  { g: 'Topo', k: 'seloNum', rot: 'Selo – número', padrao: '8' },
  { g: 'Topo', k: 'seloTxt', rot: 'Selo – texto', padrao: 'ANOS' },
  { g: 'Topo', k: 'lema', rot: 'Frase principal', padrao: 'Treinamento dos quatro elementos' },
  { g: 'Topo', k: 'lemaSub', rot: 'Frase menor', padrao: 'Venha aprender kung fu com o mestre aniversariante!' },
  { g: 'Topo', k: 'elFogo', rot: 'Elemento 1', padrao: 'FOGO' },
  { g: 'Topo', k: 'elAr', rot: 'Elemento 2', padrao: 'AR' },
  { g: 'Topo', k: 'elTerra', rot: 'Elemento 3', padrao: 'TERRA' },
  { g: 'Topo', k: 'elAgua', rot: 'Elemento 4', padrao: 'ÁGUA' },

  // Informações
  { g: 'Informações da festa', k: 'infoData', rot: 'Data', padrao: '30/11' },
  { g: 'Informações da festa', k: 'infoDataSub', rot: 'Abaixo da data', padrao: 'segunda-feira' },
  { g: 'Informações da festa', k: 'infoHora', rot: 'Horário', padrao: '16h' },
  { g: 'Informações da festa', k: 'infoHoraSub', rot: 'Abaixo do horário', padrao: 'início do treino' },
  { g: 'Informações da festa', k: 'infoLocal', rot: 'Local', padrao: 'Sítio Geranium' },
  { g: 'Informações da festa', k: 'infoLocalSub', rot: 'Abaixo do local', padrao: 'o templo' },
  { g: 'Informações da festa', k: 'dataHora', rot: 'Data e hora da contagem regressiva', padrao: '2026-11-30T16:00', tipo: 'datetime-local' },
  { g: 'Informações da festa', k: 'cdD', rot: 'Contagem – "dias"', padrao: 'dias' },
  { g: 'Informações da festa', k: 'cdH', rot: 'Contagem – "horas"', padrao: 'horas' },
  { g: 'Informações da festa', k: 'cdM', rot: 'Contagem – "min"', padrao: 'min' },
  { g: 'Informações da festa', k: 'cdS', rot: 'Contagem – "seg"', padrao: 'seg' },
  { g: 'Informações da festa', k: 'cdHoje', rot: 'Quando chegar o dia', padrao: 'É hoje! 🎉' },
  { g: 'Informações da festa', k: 'dica', rot: 'Aviso', padrao: '🥋 Venha com roupa confortável para treinar!' },

  // Formulário
  { g: 'Formulário', k: 'formTit', rot: 'Título', padrao: 'Confirme sua presença' },
  { g: 'Formulário', k: 'formSub', rot: 'Subtítulo', padrao: 'Todo discípulo precisa se inscrever no treino 🙏' },
  { g: 'Formulário', k: 'lblNome', rot: 'Rótulo do nome', padrao: 'Nome do convidado (ou da família)' },
  { g: 'Formulário', k: 'phNome', rot: 'Exemplo dentro do campo nome', padrao: 'Ex.: Família Souza' },
  { g: 'Formulário', k: 'lblVai', rot: 'Pergunta "vai?"', padrao: 'Você vai?' },
  { g: 'Formulário', k: 'btnSim', rot: 'Botão "vou"', padrao: '🥋 Vou treinar!' },
  { g: 'Formulário', k: 'btnNao', rot: 'Botão "não vou"', padrao: 'Não poderei' },
  { g: 'Formulário', k: 'lblPessoas', rot: 'Pergunta das pessoas', padrao: 'Quantas pessoas vão?' },
  { g: 'Formulário', k: 'lblPessoasSub', rot: 'Complemento da pergunta', padrao: '(conte todo mundo, inclusive você)' },
  { g: 'Formulário', k: 'criancas', rot: 'Crianças – nome', padrao: 'Crianças' },
  { g: 'Formulário', k: 'criancasSub', rot: 'Crianças – idade', padrao: 'menores de 10 anos' },
  { g: 'Formulário', k: 'adolescentes', rot: 'Adolescentes – nome', padrao: 'Adolescentes' },
  { g: 'Formulário', k: 'adolescentesSub', rot: 'Adolescentes – idade', padrao: 'de 10 a 17 anos' },
  { g: 'Formulário', k: 'adultos', rot: 'Adultos – nome', padrao: 'Adultos' },
  { g: 'Formulário', k: 'adultosSub', rot: 'Adultos – idade', padrao: '18 anos ou mais' },
  { g: 'Formulário', k: 'totalAntes', rot: 'Total – antes do número', padrao: 'Total:' },
  { g: 'Formulário', k: 'totalDepois', rot: 'Total – depois do número', padrao: 'discípulo(s)' },
  { g: 'Formulário', k: 'lblRecado', rot: 'Rótulo do recado', padrao: 'Recado para o Avatar Theo' },
  { g: 'Formulário', k: 'lblRecadoSub', rot: 'Complemento do recado', padrao: '(opcional)' },
  { g: 'Formulário', k: 'phRecado', rot: 'Exemplo dentro do recado', padrao: 'Deixe uma mensagem…' },
  { g: 'Formulário', k: 'btnEnviar', rot: 'Botão enviar (quando vai)', padrao: 'Confirmar presença' },
  { g: 'Formulário', k: 'btnEnviarNao', rot: 'Botão enviar (quando não vai)', padrao: 'Enviar resposta' },
  { g: 'Formulário', k: 'btnEnviando', rot: 'Botão enquanto envia', padrao: 'Enviando…' },
  { g: 'Formulário', k: 'erroNome', rot: 'Erro: sem nome', padrao: 'Escreva o nome do convidado 🙂' },
  { g: 'Formulário', k: 'erroPessoas', rot: 'Erro: sem pessoas', padrao: 'Conte quantas pessoas vão (use o +).' },
  { g: 'Formulário', k: 'erroEnvio', rot: 'Erro: falha no envio', padrao: 'Não deu para enviar agora. Confira a internet e tente de novo.' },

  // Confirmação
  { g: 'Tela de confirmação', k: 'okTitSim', rot: 'Título (vai)', padrao: 'Presença confirmada!' },
  { g: 'Tela de confirmação', k: 'okTxtSim', rot: 'Mensagem (vai) – use {total}', padrao: '{total} discípulo(s) inscrito(s) no treinamento. Até dia 30, às 16h!', longo: true },
  { g: 'Tela de confirmação', k: 'okTitNao', rot: 'Título (não vai)', padrao: 'Resposta enviada' },
  { g: 'Tela de confirmação', k: 'okTxtNao', rot: 'Mensagem (não vai)', padrao: 'Que pena! Obrigado por avisar. O Avatar Theo vai sentir sua falta.', longo: true },
  { g: 'Tela de confirmação', k: 'okCentro', rot: 'Número no centro da animação', padrao: '8' },
  { g: 'Tela de confirmação', k: 'btnVoltar', rot: 'Botão "alterar resposta"', padrao: 'Alterar resposta' },

  // Rodapé
  { g: 'Rodapé e aba', k: 'rodape', rot: 'Rodapé', padrao: 'Avatar Theo · 8 anos · 30 de novembro · 16h · Sítio Geranium', longo: true },
  { g: 'Rodapé e aba', k: 'tituloAba', rot: 'Título da aba do navegador', padrao: 'Avatar Theo – 8 anos' },
];

export const PADROES = Object.fromEntries(TEXTOS.map(t => [t.k, t.padrao]));
