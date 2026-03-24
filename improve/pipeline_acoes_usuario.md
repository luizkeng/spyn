# Pipeline — Ações do usuário para publicação do SPYN

> Pré-requisito: todos os arquivos já foram criados/modificados pelo Claude Code.
> Este pipeline assume que você tem acesso ao repositório GitHub como owner/admin.

---

## AÇÃO 1 — Publicar release v2.0.0 no GitHub + ativar Zenodo

**Por que isso importa:** O Zenodo detecta automaticamente novas releases do GitHub e gera um DOI novo (v2.0.0) vinculado ao conceptDOI existente (10.5281/zenodo.4019023). Sem esse DOI, o manuscrito não pode ser submetido.

**Tempo estimado:** 10–15 minutos

---

### 1.1 — Commit e push de todos os arquivos novos

No terminal (Linux, WSL, ou Git Bash no Windows):

```bash
cd /path/to/spyn   # ou o diretório local do repositório

# Verificar o que foi criado/modificado
git status

# Adicionar todos os arquivos novos (NÃO use git add -A se houver arquivos sensíveis)
git add code/spyn/__init__.py
git add code/spyn/spyn_core.py
git add code/spyn/scripts/scraping.sh
git add setup.py
git add pyproject.toml
git add requirements.txt
git add environment.yml
git add CHANGELOG.md
git add CONTRIBUTING.md
git add README.md
git add .zenodo.json
git add .github/workflows/ci.yml
git add tests/
git add examples/lamivudine/
git add docs/

# Criar o commit
git commit -m "Add packaging, tests, CI, docs and reproducible example (v2.0.0)"

# Push para o repositório remoto
git push origin master
```

**Verificar:** Acesse https://github.com/jeffrichardchemistry/spyn/actions — o workflow de CI deve aparecer rodando em poucos segundos. Aguarde ficar verde antes de continuar.

---

### 1.2 — Verificar integração Zenodo ativa

1. Acesse https://zenodo.org
2. Faça login com a conta GitHub do repositório
3. Vá em **Account → GitHub** (menu superior direito)
4. Verifique se o repositório `jeffrichardchemistry/spyn` aparece com o toggle **ON** (verde)
   - Se estiver OFF: ative-o agora
   - Se não aparecer: clique em **Sync** e aguarde alguns segundos

**Se a integração não estiver configurada:**
1. Em https://zenodo.org/account/settings/github clique em **Sync now**
2. Encontre `jeffrichardchemistry/spyn` e ative o toggle

---

### 1.3 — Criar a tag e a release v2.0.0

**Opção A — Via interface web do GitHub (mais simples):**

1. Acesse https://github.com/jeffrichardchemistry/spyn
2. Clique em **Releases** (barra lateral direita) → **Draft a new release**
3. Em **Choose a tag**, digite `v2.0.0` e selecione **Create new tag: v2.0.0 on publish**
4. Em **Target**, selecione `master`
5. **Release title:** `SPYN v2.0.0 — Publication-ready release`
6. **Description** (cole este texto):

```
## SPYN v2.0.0

This release prepares SPYN for submission to Journal of Cheminformatics.

### What's new
- `spyn_core.py`: pure-Python functions (Boltzmann, Lorentzian, GIPAW/GIAO parsers) importable without PyQt5
- Automated test suite: 34 tests, 92.86% coverage (pytest)
- GitHub Actions CI: Python 3.8 / 3.9 / 3.10
- Reproducible example: `examples/lamivudine/run_example.py` (no QE required)
- Complete documentation: installation guide, quickstart tutorial, API reference
- Python packaging: `setup.py`, `pyproject.toml`, `environment.yml`
- Comparison with related tools (CCP-NC toolbox, magresview)

### Bug fix
- `scripts/scraping.sh`: removed hardcoded developer path

### Full changelog
See [CHANGELOG.md](CHANGELOG.md)
```

7. Clique em **Publish release**

**Opção B — Via linha de comando:**
```bash
git tag -a v2.0.0 -m "SPYN v2.0.0 — Publication-ready release"
git push origin v2.0.0
# Em seguida, crie a release na interface web do GitHub a partir desta tag
```

---

### 1.4 — Confirmar geração do DOI no Zenodo

1. Aguarde 2–5 minutos após publicar a release
2. Acesse https://zenodo.org/doi/10.5281/zenodo.4019023
   - Deve aparecer uma nova versão v2.0.0
3. Anote o **novo DOI específico da v2.0.0** (formato: `10.5281/zenodo.XXXXXXX`)
4. Atualize o `.zenodo.json` se necessário (o conceptDOI 4019023 permanece o mesmo)

**Atualizar o BibTeX no README.md** com o novo DOI específico e o ano 2026:
```bibtex
@software{spyn2026,
  author  = {Dias da Silva, Jefferson Richard and
             Keng Queiroz Junior, Luiz Henrique},
  title   = {{SPYN} v2.0.0: An Open-Source Python Platform with GUI
             for NMR Crystallography},
  year    = {2026},
  doi     = {10.5281/zenodo.XXXXXXX},   ← substituir pelo DOI real da v2.0.0
  url     = {https://github.com/jeffrichardchemistry/spyn},
  license = {GPL-3.0}
}
```

---

## AÇÃO 2 — Configurar Codecov (badge de cobertura de testes)

**Por que isso importa:** Journal of Cheminformatics e JOSS exigem evidência de CI ativo. O badge de cobertura no README é a forma padrão de demonstrar isso.

**Tempo estimado:** 5 minutos

---

### 2.1 — Ativar repositório no Codecov

1. Acesse https://codecov.io
2. Clique em **Sign in with GitHub**
3. Autorize o Codecov a acessar sua conta
4. Na dashboard, procure `jeffrichardchemistry/spyn`
   - Se não aparecer: clique em **Add new repository** → selecione `spyn`
5. Clique no repositório — aparecerá uma tela com instruções

---

### 2.2 — Adicionar token ao GitHub Secrets

O CI já está configurado para enviar o relatório de cobertura (`codecov-action@v4`).
Para repositórios **privados** o token é obrigatório; para **públicos** é opcional mas recomendado.

1. No Codecov, copie o **CODECOV_TOKEN** exibido na tela de configuração do repositório
2. Acesse https://github.com/jeffrichardchemistry/spyn/settings/secrets/actions
3. Clique em **New repository secret**
   - **Name:** `CODECOV_TOKEN`
   - **Secret:** cole o token copiado
4. Clique em **Add secret**

---

### 2.3 — Adicionar badge ao README.md

Após o primeiro CI rodar com sucesso, o Codecov gera a URL do badge.
No Codecov, vá em **Settings → Badge** e copie o markdown. Será algo como:

```
[![codecov](https://codecov.io/gh/jeffrichardchemistry/spyn/branch/master/graph/badge.svg)](https://codecov.io/gh/jeffrichardchemistry/spyn)
```

Adicione esta linha no topo do `README.md`, após o badge de CI:

```markdown
[![CI](https://github.com/jeffrichardchemistry/spyn/actions/workflows/ci.yml/badge.svg)](...)
[![codecov](https://codecov.io/gh/jeffrichardchemistry/spyn/branch/master/graph/badge.svg)](...)  ← adicionar aqui
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4019023.svg)](...)
```

---

## AÇÃO 3 — Ajustes no manuscrito

**Por que isso importa:** Journal of Cheminformatics exige explicitamente uma seção comparando o software com ferramentas relacionadas, e a tabela de "Availability and Requirements" deve incluir CI e testes.

**Tempo estimado:** 30–60 minutos

---

### 3.1 — Adicionar seção "Comparison with existing tools"

Em **Results and Discussion** (ou seção equivalente), adicione uma subseção com este conteúdo adaptado ao estilo do manuscrito:

**Título sugerido:** *"Comparison with existing software for solid-state NMR analysis"*

**Parágrafo 1 — Estado da arte:**
> The CCP-NC toolbox [REF] provides Python scripts for processing solid-state NMR data in the `.magres` format produced by CASTEP, but requires command-line operation and has no conformational search or Boltzmann analysis capabilities. The magresview software [REF] offers a graphical interface for visualising NMR tensors in `.magres` files but does not perform GIPAW calculations or spectral broadening. Both tools target users already familiar with computational NMR workflows.

**Parágrafo 2 — Tabela de comparação:**
Inserir a tabela de `docs/comparison.md` (seção "Feature comparison").

**Parágrafo 3 — Benchmark de usabilidade:**
> A complete GIPAW shielding tensor calculation using the manual workflow requires at least 11 sequential steps, demanding expertise in QE input syntax, Linux command-line operations, and NMR crystallography conventions. SPYN accomplishes the same task in 6 GUI interactions with no knowledge of QE input files required (Table X / Figure X).

**Referências a incluir:**
- Szell PMJ et al. (2021) Solid State NMR 115, 101733 — CCP-NC toolbox
- Hanwell MD et al. (2012) J Cheminformatics 4:17 — magresview

---

### 3.2 — Atualizar tabela "Availability and Requirements"

Localize a tabela padrão do Journal of Cheminformatics e atualize/adicione as linhas:

| Field | Value |
|-------|-------|
| **Name** | SPYN |
| **Version** | 2.0.0 |
| **Operating system(s)** | Linux (Debian/Ubuntu/Mint) |
| **Programming language** | Python 3.6+ |
| **Other requirements** | PyQt5 ≥ 5.12, NumPy, SciPy, Pandas, Matplotlib, OpenBabel ≥ 3.0, Quantum ESPRESSO ≥ 6.3 (optional) |
| **License** | GPL-3.0 |
| **Restrictions to use by non-academics** | None |
| **Source code** | https://github.com/jeffrichardchemistry/spyn |
| **DOI** | 10.5281/zenodo.XXXXXXX *(DOI da v2.0.0 — preencher após Ação 1)* |
| **Unit tests** | Yes (pytest, 34 tests, 92.86% coverage) |
| **CI/CD** | Yes (GitHub Actions, Python 3.8/3.9/3.10) |
| **Example dataset** | Yes (`examples/lamivudine/`, no QE required) |

---

### 3.3 — Atualizar abstract e keywords (verificação)

- [ ] Abstract ≤ 350 palavras (contar)
- [ ] Incluir os termos: "GIPAW", "conformational search", "Boltzmann", "open-source", "GUI"
- [ ] Keywords (3–10 termos): NMR crystallography, GIPAW, GIAO, solid-state NMR, conformational search, Boltzmann distribution, Quantum ESPRESSO, Python

---

### 3.4 — Adicionar badges ao manuscrito

Na seção **Availability**, adicione as URLs:
- CI badge: `https://github.com/jeffrichardchemistry/spyn/actions/workflows/ci.yml`
- Coverage badge: `https://codecov.io/gh/jeffrichardchemistry/spyn` *(após Ação 2)*
- DOI badge: `https://doi.org/10.5281/zenodo.XXXXXXX` *(após Ação 1)*

---

## Checklist geral pré-submissão

```
□ AÇÃO 1: CI passou (verde) no GitHub Actions
□ AÇÃO 1: DOI v2.0.0 gerado no Zenodo
□ AÇÃO 1: BibTeX atualizado no README com novo DOI
□ AÇÃO 2: Badge Codecov no README (mostrando ≥ 80%)
□ AÇÃO 3: Seção de comparação no manuscrito
□ AÇÃO 3: Tabela Availability atualizada
□ AÇÃO 3: Abstract ≤ 350 palavras verificado
□ AÇÃO 3: DOI v2.0.0 no manuscrito
□ Executar: python examples/lamivudine/run_example.py (confirmar que gera PNG)
□ Executar: pytest tests/ -v --cov=spyn (confirmar 34/34 + ≥ 80% coverage)
```
