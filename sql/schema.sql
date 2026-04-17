-- ============================================================
-- MINI-GAME ENIGMA — Schema SQL para Supabase
-- Execute no SQL Editor do Supabase (Project > SQL Editor)
-- ============================================================

-- ──────────────────────────────────────────────────────────
-- EXTENSIONS
-- ──────────────────────────────────────────────────────────
create extension if not exists "pgcrypto";

-- ──────────────────────────────────────────────────────────
-- ENUMS
-- ──────────────────────────────────────────────────────────
create type dificuldade_enum as enum ('facil', 'medio', 'dificil');
create type status_rodada_enum as enum ('em_andamento', 'vitoria', 'derrota');

-- ──────────────────────────────────────────────────────────
-- TABELA: usuarios
-- ──────────────────────────────────────────────────────────
create table if not exists usuarios (
    id          uuid primary key default gen_random_uuid(),
    username    text not null unique,
    email       text not null unique,
    senha_hash  text not null,
    pontuacao_total int not null default 0,
    created_at  timestamptz not null default now()
);

-- ──────────────────────────────────────────────────────────
-- TABELA: enigmas
-- ──────────────────────────────────────────────────────────
create table if not exists enigmas (
    id                uuid primary key default gen_random_uuid(),
    titulo            text not null,
    descricao         text not null,
    resposta_correta  text not null,
    dica_1            text,
    dica_2            text,
    dica_3            text,
    dificuldade       dificuldade_enum not null default 'medio',
    pontuacao_inicial int not null,
    ativo             boolean not null default true,
    created_at        timestamptz not null default now(),
    constraint chk_pontuacao check (pontuacao_inicial in (5000, 10000, 15000))
);

-- ──────────────────────────────────────────────────────────
-- TABELA: rodadas
-- ──────────────────────────────────────────────────────────
create table if not exists rodadas (
    id              uuid primary key default gen_random_uuid(),
    usuario_id      uuid not null references usuarios(id) on delete cascade,
    enigma_id       uuid not null references enigmas(id) on delete cascade,
    pontuacao_atual int not null,
    dicas_usadas    int not null default 0 check (dicas_usadas between 0 and 3),
    status          status_rodada_enum not null default 'em_andamento',
    created_at      timestamptz not null default now(),
    finalizada_at   timestamptz
);

-- ──────────────────────────────────────────────────────────
-- TABELA: tentativas
-- ──────────────────────────────────────────────────────────
create table if not exists tentativas (
    id                  uuid primary key default gen_random_uuid(),
    rodada_id           uuid not null references rodadas(id) on delete cascade,
    resposta_usuario    text not null,
    feedback_ia         text,
    correta             boolean not null default false,
    penalidade_aplicada int not null default 0,
    created_at          timestamptz not null default now()
);

-- ──────────────────────────────────────────────────────────
-- ÍNDICES
-- ──────────────────────────────────────────────────────────
create index if not exists idx_rodadas_usuario  on rodadas(usuario_id);
create index if not exists idx_rodadas_enigma   on rodadas(enigma_id);
create index if not exists idx_tentativas_rodada on tentativas(rodada_id);
create index if not exists idx_usuarios_pontuacao on usuarios(pontuacao_total desc);

-- ──────────────────────────────────────────────────────────
-- ROW LEVEL SECURITY (RLS)
-- Desabilitado para simplificar — habilite em produção
-- ──────────────────────────────────────────────────────────
alter table usuarios    disable row level security;
alter table enigmas     disable row level security;
alter table rodadas     disable row level security;
alter table tentativas  disable row level security;

-- ──────────────────────────────────────────────────────────
-- SEED — Enigmas de Exemplo
-- ──────────────────────────────────────────────────────────
insert into enigmas (titulo, descricao, resposta_correta, dica_1, dica_2, dica_3, dificuldade, pontuacao_inicial) values
(
    'O Guardião do Tempo',
    'Tenho ponteiros, mas não tenho mãos. Faço tique-taque, mas não tenho coração. O que sou eu?',
    'relógio',
    'Você me encontra em quartos e pulsos.',
    'Tenho 12 números no meu rosto.',
    'Meço horas, minutos e segundos.',
    'facil', 5000
),
(
    'A Eterna Chama',
    'Quanto mais me alimentas, mais crescerei. Quanto mais água me deres, mais morrerei. O que sou eu?',
    'fogo',
    'Sou visível no escuro.',
    'Dou calor e luz.',
    'Combustíveis me fazem maior.',
    'medio', 10000
),
(
    'Vivo sem corpo',
    'Falo sem língua, ouço sem ouvidos, não tenho corpo, mas ganho vida com o vento. O que sou eu?',
    'eco',
    'Minha voz é a repetição da sua.',
    'Você me ouve em montanhas e cavernas.',
    'Sou o som que volta.',
    'medio', 10000
),
(
    'O Paradoxo do Pai',
    'Um homem olha para um retrato e diz: "Não tenho irmãos nem irmãs, mas o pai desse homem é filho do meu pai." De quem é o retrato?',
    'filho',
    'Pense nas relações familiares diretas.',
    'O homem está relacionado à pessoa no retrato.',
    'A pessoa no retrato é uma geração abaixo.',
    'dificil', 15000
),
(
    'O Retrato do Silêncio',
    'O que você pode quebrar sem tocá-lo ou vê-lo?',
    'silêncio',
    'Não precisa de força física.',
    'Você pode fazer isso falando.',
    'Está em salas vazias e bibliotecas.',
    'facil', 5000
),
(
    'Nascido da Terra',
    'Sou branco quando sujo e preto quando limpo. O que sou eu?',
    'lousa',
    'Sou encontrado em salas de aula.',
    'Você escreve e apaga em mim.',
    'Antes das lousa brancas, eu dominava as escolas.',
    'medio', 10000
),
(
    'O Peso do Vazio',
    'O que é cheio de buracos, mas ainda consegue segurar água?',
    'esponja',
    'É poroso por natureza.',
    'Usado na cozinha e no banho.',
    'Absorvo líquidos facilmente.',
    'facil', 5000
),
(
    'O Livro Eterno',
    'Tenho cidades, mas nelas não moram pessoas. Tenho montanhas, mas não têm árvores. Tenho água, mas nela não vivem peixes. Tenho estradas, mas por elas não passam carros. O que sou eu?',
    'mapa',
    'Sou uma representação do mundo.',
    'Viajantes me usam para se orientar.',
    'Posso ser físico ou digital.',
    'dificil', 15000
);
