# SPYN — Publication Readiness Pipeline
> Pipeline para Claude Code | Alvo: Journal of Cheminformatics (IF 5.7) e SoftwareX (IF 2.7)
> Repositório: https://github.com/jeffrichardchemistry/spyn | DOI Zenodo atual: 10.5281/zenodo.4019024

---

## Estado atual do repositório (diagnóstico)

| Item | Estado | Impacto na submissão |
|---|---|---|
| Código-fonte | ✅ Disponível em `code/spyn/` (17 py + 4 sh) | OK |
| Licença GPL-3.0 | ✅ `LICENSE` presente | OK |
| README básico | ⚠️ Mínimo — só instalação | Desk rejection risk |
| Testes automatizados | ❌ Inexistentes | Bloqueador (JOSS/JCheminf) |
| CI/CD (GitHub Actions) | ❌ Inexistente | Bloqueador (JOSS/JCheminf) |
| Documentação técnica | ❌ Inexistente | Major revision garantida |
| Zenodo v2 atualizado | ❌ v1.0 de 2020 sem descrição | APC waiver em risco |
| Comparação com tools similares | ❌ Inexistente | Desk rejection (JCheminf) |
| Reprodutibilidade (Docker/conda) | ❌ Inexistente | Major revision garantida |
| Cross-platform | ❌ Linux-only | Fraqueza aceitável para v2 |

---

## Estrutura do pipeline

```
FASE 1 — Repositório e qualidade de software     (~2 semanas)
FASE 2 — Reprodutibilidade e ambiente             (~1 semana)
FASE 3 — Testes automatizados e CI               (~2 semanas)
FASE 4 — Documentação técnica                    (~1 semana)
FASE 5 — Comparação com softwares relacionados   (~1 semana)
FASE 6 — Registro Zenodo v2 e material supl.     (~2 dias)
FASE 7 — Ajustes finais no manuscrito            (~3 dias)
```

**Tempo total estimado:** 7–8 semanas de trabalho real  
**Pré-requisito para Claude Code:** clonar o repositório localmente antes de iniciar cada fase

---

## FASE 1 — Reestruturação do repositório

### Objetivo
Transformar a estrutura atual em um projeto Python moderno e publicável, compatível com os padrões esperados por revisores de software de periódicos científicos.

### 1.1 Reorganização da estrutura de diretórios

**Instrução para Claude Code:**
```
Reorganize o repositório jeffrichardchemistry/spyn com a seguinte estrutura-alvo.
O código atual está em code/spyn/ com 17 arquivos .py e 4 .sh.
Mantenha todo o código existente, apenas reposicione os arquivos e crie os novos 
arquivos de configuração vazios listados abaixo.
```

**Estrutura-alvo:**
```
spyn/
├── spyn/                          # pacote Python principal
│   ├── __init__.py                # CRIAR — versão, autores, DOI
│   ├── conformer/                 # MOVER módulos de busca conformacional
│   │   └── __init__.py
│   ├── boltzmann/                 # MOVER módulo de distribuição
│   │   └── __init__.py
│   ├── ssnmr/                     # MOVER módulos GIPAW/SCF
│   │   └── __init__.py
│   ├── spectro/                   # MOVER módulos de visualização espectral
│   │   └── __init__.py
│   └── utils/                     # MOVER utilitários (parsing, Lorentz, etc.)
│       └── __init__.py
├── tests/                         # CRIAR (vazio agora — preenchido na Fase 3)
│   ├── __init__.py
│   ├── test_boltzmann.py
│   ├── test_lorentz.py
│   ├── test_parser_gipaw.py
│   └── test_parser_giao.py
├── docs/                          # CRIAR (preenchido na Fase 4)
│   ├── installation.md
│   ├── quickstart.md
│   ├── modules/
│   └── examples/
├── examples/                      # CRIAR
│   ├── README.md
│   └── lamivudine/                # dados de exemplo (CIF público + saída QE mock)
├── .github/
│   └── workflows/
│       └── ci.yml                 # CRIAR na Fase 3
├── environment.yml                # CRIAR na Fase 2
├── requirements.txt               # CRIAR
├── setup.py                       # CRIAR
├── pyproject.toml                 # CRIAR
├── CHANGELOG.md                   # CRIAR
├── CONTRIBUTING.md                # CRIAR
├── CODE_OF_CONDUCT.md             # CRIAR
├── LICENSE                        # JÁ EXISTE — manter
└── README.md                      # ATUALIZAR completamente (Fase 4)
```

### 1.2 Criar `setup.py` e `pyproject.toml`

**Instrução para Claude Code:**
```
Crie setup.py e pyproject.toml para o pacote spyn com base no código existente.
Inspecione os imports nos arquivos .py em code/spyn/ para extrair as dependências reais.
Use setuptools. Nome do pacote: spyn. Versão: 2.0.0.
```

**Conteúdo esperado do `setup.py`:**
```python
from setuptools import setup, find_packages

setup(
    name='spyn',
    version='2.0.0',
    author='Jefferson Richard Dias da Silva, Luiz Henrique Keng Queiroz Júnior',
    author_email='lhkengqueiroz@ufg.br',
    description='GUI platform for NMR crystallography workflows (GIPAW/GIAO/Conformer Search)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jeffrichardchemistry/spyn',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'PyQt5>=5.12',
        'pandas>=0.25',
        'numpy>=1.17',
        'scipy>=1.3',
        'matplotlib>=3.1',
    ],
    entry_points={
        'console_scripts': ['spyn=spyn.__main__:main'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics',
    ],
)
```

### 1.3 Criar `CHANGELOG.md`

**Instrução para Claude Code:**
```
Crie CHANGELOG.md no formato Keep a Changelog (https://keepachangelog.com).
Documente a v1.0.0 (setembro 2020) com base nas funcionalidades descritas na 
dissertação de Jefferson Richard Dias da Silva (UFG, 2021).
Crie entrada para v2.0.0 [Unreleased] com os itens deste pipeline como planned.
```

---

## FASE 2 — Reprodutibilidade e ambiente isolado

### Objetivo
Garantir que qualquer revisor — em qualquer máquina Linux — consiga reproduzir os resultados do artigo sem instalar dependências manualmente.

### 2.1 Criar `environment.yml` (conda)

**Instrução para Claude Code:**
```
Crie environment.yml para conda com todas as dependências do spyn.
Nome do ambiente: spyn-env. Python 3.8 (compatível com 3.6+ e mais estável em 2024).
Inclua canal conda-forge para openbabel.
Quantum-Espresso NÃO deve estar no environment.yml — adicione comentário 
explicando que QE deve ser instalado separadamente conforme docs/installation.md.
```

**Conteúdo esperado:**
```yaml
name: spyn-env
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.8
  - pyqt=5.12
  - pandas>=0.25
  - numpy>=1.17
  - scipy>=1.3
  - matplotlib>=3.1
  - openbabel>=3.0          # via conda-forge
  - pip
  - pip:
    - spyn                  # instala o pacote local com: pip install -e .
# NOTE: Quantum-Espresso >= 6.3 must be installed separately.
# See docs/installation.md for step-by-step instructions.
# Pseudopotentials: pbe-tm-new-gipaw-dc (download from http://www.gipaw.net)
```

### 2.2 Criar exemplo reprodutível sem QE real (dados mock)

**Instrução para Claude Code:**
```
Crie o diretório examples/lamivudine/ com os seguintes arquivos:
1. README.md explicando o exemplo end-to-end
2. lamivudine_formII.cif — arquivo CIF público da Lamivudina Forma II 
   (CSD refcode LAMVUD ou equivalente disponível sem paywall — use o CIF 
   disponível em https://www.ccdc.cam.ac.uk/structures/Search?Refcode=LAMVUD 
   ou gere um CIF sintético simplificado com a estrutura conhecida)
3. mock_gipaw_output.txt — saída simulada de GIPAW-QE para a lamivudina 
   com os tensores de blindagem reais da Tabela 6.1 da dissertação 
   (8 átomos de carbono, valores δ_calc GIPAW da Forma II)
4. mock_scf_output.txt — saída simulada de SCF convergida
5. run_example.py — script que demonstra o módulo de Boltzmann e o módulo 
   de Lorentz SEM necessitar de QE instalado, usando os arquivos mock
```

**O arquivo `run_example.py` deve:**
- Importar os módulos `spyn.boltzmann` e `spyn.spectro`
- Calcular a distribuição de Boltzmann para 5 confôrmeros sintéticos
- Gerar o espectro teórico de 13C da lamivudina a partir do mock_gipaw_output.txt
- Salvar a figura como `example_spectrum.png`
- Executar completamente sem PyQt5 (modo headless)
- Completar em < 30 segundos em hardware comum

---

## FASE 3 — Testes automatizados e integração contínua

### Objetivo
Implementar cobertura de testes unitários para os módulos Python puros do SPYN (sem dependência de QE ou GUI) e configurar CI/CD via GitHub Actions.

### 3.1 Testes unitários — módulo Boltzmann

**Instrução para Claude Code:**
```
Inspecione o código de distribuição de Boltzmann em code/spyn/ (provavelmente 
em um arquivo chamado boltzmann.py ou similar).
Crie tests/test_boltzmann.py com pytest cobrindo:
1. Resultado numérico correto para entrada simples conhecida
2. Invariância à escala de energias (somar constante a todas as energias 
   não muda as populações)
3. Soma das populações = 1.0 (conservação)
4. Conformer de menor energia tem maior população (T > 0)
5. Limite T → ∞: todas as populações iguais
6. Comportamento com energia negativa (kcal/mol)
7. Comportamento com lista de 1 confôrmero
8. TypeError para entrada não-numérica
```

**Template de teste esperado:**
```python
import pytest
import numpy as np
from spyn.boltzmann import boltzmann_distribution   # ajustar import conforme código real

class TestBoltzmannDistribution:
    
    def test_sum_to_one(self):
        energies = [0.0, 1.0, 2.0, 5.0]
        pops = boltzmann_distribution(energies, T=298.15)
        assert abs(sum(pops) - 1.0) < 1e-10
    
    def test_lowest_energy_most_populated(self):
        energies = [0.0, 2.0, 5.0]
        pops = boltzmann_distribution(energies, T=298.15)
        assert pops[0] == max(pops)
    
    def test_energy_shift_invariance(self):
        energies = [0.0, 1.0, 3.0]
        shifted  = [e + 100.0 for e in energies]
        pops1 = boltzmann_distribution(energies, T=298.15)
        pops2 = boltzmann_distribution(shifted, T=298.15)
        np.testing.assert_allclose(pops1, pops2, rtol=1e-8)
    
    def test_single_conformer(self):
        pops = boltzmann_distribution([0.0], T=298.15)
        assert abs(pops[0] - 1.0) < 1e-10
    
    def test_known_result(self):
        # 2 conformers, ΔE = kT → ratio ≈ e ≈ 2.718
        k  = 0.001987204  # kcal/(mol·K)
        T  = 298.15
        dE = k * T        # ΔE = 1 kT
        energies = [0.0, dE]
        pops = boltzmann_distribution(energies, T=T)
        assert abs(pops[0] / pops[1] - np.e) < 0.01
```

### 3.2 Testes unitários — módulo Lorentz

**Instrução para Claude Code:**
```
Inspecione o código da distribuição Lorentziana em code/spyn/.
Crie tests/test_lorentz.py com pytest cobrindo:
1. Valor no máximo (x = x0) igual a h
2. Valor em x = x0 ± l/2 igual a h/2 (definição de FWHM)
3. A curva é simétrica em torno de x0
4. Integral numérica converge para πlh/2 (integral analítica da Lorentziana)
5. Comportamento com múltiplos picos (superposição linear)
6. FWHM = 0 deve lançar exceção ou retornar spike em x0
```

### 3.3 Testes unitários — parser de output GIPAW

**Instrução para Claude Code:**
```
Inspecione o código de parsing da saída do GIPAW em code/spyn/.
Use o arquivo examples/lamivudine/mock_gipaw_output.txt como fixture.
Crie tests/test_parser_gipaw.py com pytest cobrindo:
1. O parser extrai o número correto de átomos (8 carbonos na lamivudina)
2. Os tensores σ_iso extraídos batem com os valores esperados (±0.01 ppm)
3. O parser lida com arquivo de saída vazio (retorna lista vazia, não exception)
4. O parser lida com arquivo truncado (QE terminou por erro) — deve lançar 
   ParseError específico, não crash genérico
5. O mapeamento átomo → elemento → σ_iso está correto
6. A conversão σ_iso → δ (usando referência da glicina = 173.0 ppm) 
   produz o deslocamento químico correto para C1 da lamivudina (≈ 167.2 ppm)
```

### 3.4 Testes unitários — parser de output GIAO (Gaussian)

**Instrução para Claude Code:**
```
Inspecione o código de parsing de arquivos .log do Gaussian em code/spyn/.
Crie um mock_gaussian_output.log baseado nos valores de δ_calc(GIAO) 
da Tabela 6.1 da dissertação para a Forma II da lamivudina.
Crie tests/test_parser_giao.py com pytest cobrindo os mesmos 6 casos 
do test_parser_gipaw.py, adaptados para o formato de saída do Gaussian09.
```

### 3.5 Configurar GitHub Actions (CI)

**Instrução para Claude Code:**
```
Crie .github/workflows/ci.yml para rodar os testes automaticamente em 
cada push e pull request.
Requisitos:
- Ubuntu latest
- Python 3.8
- Instalar dependências via pip (sem QE — testes não precisam dele)
- Rodar pytest com coverage
- Fazer upload do relatório de cobertura para Codecov (opcional)
- Badge de status deve aparecer no README
```

**Conteúdo esperado do `ci.yml`:**
```yaml
name: CI

on:
  push:
    branches: [ master, main, develop ]
  pull_request:
    branches: [ master, main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10"]

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest pytest-cov
        pip install numpy scipy pandas matplotlib
        pip install -e .
    
    - name: Run tests
      run: |
        pytest tests/ -v --cov=spyn --cov-report=xml --cov-report=term-missing
    
    - name: Upload coverage
      uses: codecov/codecov-action@v4
      with:
        file: ./coverage.xml
```

**Meta de cobertura mínima aceitável para submissão:**
- `test_boltzmann.py`: 100% das funções públicas
- `test_lorentz.py`: 100% das funções públicas  
- `test_parser_gipaw.py`: ≥ 80% das linhas do parser
- `test_parser_giao.py`: ≥ 80% das linhas do parser
- Cobertura total do pacote: ≥ 60%

---

## FASE 4 — Documentação técnica completa

### Objetivo
Produzir documentação que permita a um revisor instalar, executar e avaliar o SPYN sem assistência.

### 4.1 README.md completo

**Instrução para Claude Code:**
```
Reescreva README.md completamente. Deve conter:
1. Badge de CI (GitHub Actions), badge de cobertura (Codecov), 
   badge DOI (Zenodo), badge de licença GPL-3.0
2. Seção "What is SPYN" — 3 parágrafos descrevendo o problema resolvido e 
   as 4 funcionalidades principais (conformer search, Boltzmann, GIPAW, Spectro)
3. Seção "Quick install" — conda em 3 comandos
4. Seção "Quick start" — reproduzir o exemplo da lamivudina em 5 passos
5. Seção "Requirements" — tabela: Python ≥3.6, QE ≥6.3, OpenBabel ≥3.0, 
   Jmol, Linux (Debian-based ou RPM-based)
6. Seção "Documentation" — link para docs/
7. Seção "How to cite" — BibTeX do artigo + DOI Zenodo
8. Seção "Contributing" — link para CONTRIBUTING.md
9. Screenshot das 4 abas principais (use os PNGs já extraídos da dissertação)
```

### 4.2 `docs/installation.md` — guia detalhado

**Instrução para Claude Code:**
```
Crie docs/installation.md com guia de instalação passo a passo testado em:
- Ubuntu 20.04 LTS
- Linux Mint 20
- Debian 11

Cobrindo:
1. Pré-requisitos do sistema (apt install)
2. Instalação do conda/miniconda (se não tiver)
3. Criação do ambiente conda via environment.yml
4. Compilação e instalação do Quantum-Espresso 6.3 com suporte a GIPAW
   (ou instalação via symlink de versão externa)
5. Download dos pseudopotenciais pbe-tm-new-gipaw-dc
6. Teste de instalação: executar run_example.py e verificar que gera 
   example_spectrum.png sem erros
7. Seção de troubleshooting com os 5 erros mais comuns (baseados no 
   texto da dissertação e na experiência descrita no README atual)
```

### 4.3 `docs/quickstart.md` — tutorial guiado

**Instrução para Claude Code:**
```
Crie docs/quickstart.md como um tutorial em 4 seções, cada uma 
correspondendo a uma aba do SPYN:

Seção 1: Conformational Searching
- Screenshot da aba (fig_conformer_crop.png)
- Passo a passo: importar CIF, configurar parâmetros, executar, exportar

Seção 2: Boltzmann Distribution  
- Screenshot da aba (fig_boltzmann_crop.png)
- Passo a passo: modo automático (após busca conformacional) e modo manual

Seção 3: ss-NMR (GIPAW)
- Screenshot das abas (fig_ssnmr_crop.png, fig_filter_crop.png)
- Passo a passo: importar CIF, configurar parâmetros QE, executar SCF, 
  executar GIPAW, inspecionar output filtrado

Seção 4: Spectro-NMR
- Screenshot da aba (fig_spectro_crop.png, fig_sticks_crop.png)
- Passo a passo: carregar resultado GIPAW, definir referência, 
  aplicar Lorentziana, exportar espectro

Use os screenshots já extraídos da dissertação como figuras inline.
```

### 4.4 `docs/modules/` — documentação da API

**Instrução para Claude Code:**
```
Para cada módulo Python identificado em code/spyn/, crie uma página .md em 
docs/modules/ documentando:
- Propósito do módulo (1 parágrafo)
- Classes principais com seus parâmetros de __init__
- Métodos públicos com assinaturas e docstrings
- Exemplo mínimo de uso (código Python)

Prioridade: boltzmann.py, lorentz.py, parser_gipaw.py, parser_giao.py
```

---

## FASE 5 — Comparação com softwares relacionados

### Objetivo
Produzir a evidência de avanço sobre o estado da arte exigida explicitamente pela Journal of Cheminformatics.

### 5.1 Tabela de comparação de funcionalidades

**Instrução para Claude Code:**
```
Crie uma tabela de comparação de funcionalidades entre SPYN e as 
ferramentas relacionadas existentes. Use as informações abaixo e 
preencha com base no conhecimento técnico do código do SPYN.

Ferramentas a comparar:
1. SPYN (este trabalho)
2. CCP-NC toolbox (Szell et al., 2021, Solid State NMR)
   - CLI scripts only, sem GUI
   - Integração com Materials Studio e TopSpin
   - Suporta formato .magres do CASTEP
   - Sem conformational search
   - Sem Boltzmann distribution
3. magresview (Hanwell et al., 2012, J Cheminformatics)
   - GUI para visualização de tensores .magres
   - Sem cálculo GIPAW integrado
   - Sem conformational search
   - Sem Boltzmann distribution
   - Sem overlay experimental/teórico
4. Workflow manual QE + scripts in-house
   - Linha de comando pura
   - Curva de aprendizado: alta

Critérios da tabela:
- GUI disponível
- Conformational search integrado
- Boltzmann population analysis
- GIPAW calculations (integrado, não externo)
- GIAO result import
- Lorentzian broadening
- Experimental/theoretical overlay
- Formatos de entrada suportados (CIF, mol, xyz, etc.)
- Output export formats (PDF, SVG, PNG)
- Licença
- OS suportados
- Linguagem de implementação
- Curva de aprendizado (subjetivo: baixa/média/alta)
- Disponível sem login/paywall

Formato de saída: tabela Markdown + versão LaTeX para o suplementar do artigo.
```

### 5.2 Benchmarking de usabilidade (workflow steps count)

**Instrução para Claude Code:**
```
Documente o número de etapas necessárias para completar um cálculo 
completo de tensores de blindagem GIPAW para um composto novo usando:

(A) Workflow manual (QE puro):
1. Obter arquivo CIF do CSD
2. Converter CIF para formato QE com cif2qe ou script manual
3. Baixar pseudopotencial correto
4. Editar manualmente o arquivo de input SCF (iberwave, k-points, etc.)
5. Executar pw.x via terminal
6. Verificar convergência no output (grep manual)
7. Editar manualmente o arquivo de input GIPAW
8. Executar gipaw.x via terminal
9. Parsear o output (grep ou script manual) para extrair σ_iso
10. Calcular δ = σ_ref − σ_iso manualmente
11. Plotar espectro (matplotlib script ou outro software)
Total: ≥ 11 etapas com alto conhecimento técnico necessário

(B) SPYN:
1. Abrir SPYN
2. File → Import CIF
3. Configurar parâmetros na aba ss-NMR (3 campos numéricos)
4. Clicar "Calculate SCF"
5. Clicar "Calculate GIPAW"
6. Ir para aba Spectro-NMR → inserir referência → clicar "Plot"
Total: 6 etapas, conhecimento técnico mínimo necessário

Esta comparação deve aparecer como seção "Usability benchmark" no artigo 
e como figura adicional (diagrama de fluxo antes/depois) no suplementar.
```

### 5.3 Gerar figura de comparação de workflow

**Instrução para Claude Code:**
```
Crie um script Python (docs/figures/generate_workflow_comparison.py) que 
produza uma figura de dois painéis lado a lado mostrando:
- Painel esquerdo: fluxo de trabalho manual (11 etapas em caixas vermelhas)
- Painel direito: fluxo de trabalho no SPYN (6 etapas em caixas verdes)
Use matplotlib. Salve como workflow_comparison.pdf e workflow_comparison.png.
Estilo: fundo branco, fonte Arial 10pt, setas pretas, compatível com 
os padrões de figuras do Journal of Cheminformatics.
```

---

## FASE 6 — Atualização do Zenodo e material suplementar

### Objetivo
Criar o DOI de versão 2.0.0 no Zenodo com metadados completos e arquivar o material suplementar do artigo.

### 6.1 Atualizar metadados do Zenodo

**Instrução para Claude Code:**
```
Crie o arquivo .zenodo.json com os metadados completos para a v2.0.0 do SPYN.
Este arquivo é lido automaticamente pelo Zenodo quando o repositório 
GitHub tem integração ativa.

Campos obrigatórios:
- title: "SPYN v2.0.0: An Open-Source Python Platform with GUI for NMR Crystallography"
- description: parágrafo do abstract do artigo
- creators: Jefferson Richard Dias da Silva (ORCID se disponível) e 
             Luiz Henrique Keng Queiroz Júnior (ORCID: verificar)
- keywords: lista de 10 termos relevantes
- license: GPL-3.0
- related_identifiers: DOI do artigo no Journal of Cheminformatics (placeholder)
- communities: zenodo (default)
- version: "2.0.0"
- upload_type: software
```

### 6.2 Criar material suplementar do artigo

**Instrução para Claude Code:**
```
Crie docs/supplementary/supplementary_information.md com:

S1. Tabela completa de comparação de funcionalidades (da Fase 5.1)
S2. Workflow de instalação detalhado (com comandos exatos)
S3. Tabela completa de parâmetros QE usados nos cálculos da lamivudina
    (ecutwfc, k-points, pseudopotencial, convergência)
S4. Figura do workflow de comparação (da Fase 5.3)
S5. Listagem dos 17 módulos Python do SPYN com descrição de 1 linha cada
S6. Resultados completos do exemplo reprodutível (outputs do run_example.py)
S7. Instruções para revisores: como instalar e testar o SPYN em 10 minutos
    usando o ambiente conda e o exemplo da lamivudina sem precisar de QE real

O suplementar deve ser auto-suficiente: um revisor deve conseguir avaliar 
o software lendo apenas o suplementar, sem precisar contactar os autores.
```

---

## FASE 7 — Ajustes finais no manuscrito

### Objetivo
Incorporar ao manuscrito do artigo os resultados das fases anteriores.

### 7.1 Adicionar seção de comparação ao manuscrito

**Instrução para Claude Code:**
```
No arquivo SPYN_JCheminformatics.docx (ou na versão .md do manuscrito), 
adicione uma nova subseção em "Results and Discussion" com título 
"Comparison with existing tools".

Conteúdo:
- 2 parágrafos descrevendo CCP-NC toolbox e magresview como o estado da arte
- A tabela de comparação de funcionalidades (da Fase 5.1)
- A contagem de etapas do benchmark de usabilidade (da Fase 5.2)
- 1 parágrafo de síntese: o que o SPYN oferece que os outros não oferecem

Referências a adicionar:
- Szell PMJ et al. (2021) Solid State NMR — CCP-NC toolbox
- Hanwell MD et al. (2012) J Cheminformatics — magresview
```

### 7.2 Adicionar badge de CI e cobertura ao manuscrito

**Instrução para Claude Code:**
```
Adicione ao manuscrito (seção Availability and Requirements) os badges de:
- GitHub Actions CI: passing/failing
- Codecov coverage: %
- Zenodo DOI: link para v2.0.0

E adicione à tabela de Availability:
- Unit tests: Yes (pytest, 4 test modules, ≥60% coverage)
- CI/CD: Yes (GitHub Actions, Python 3.8/3.9/3.10)
- Example dataset: Yes (lamivudine CIF + mock GIPAW output, doi:10.5281/zenodo.XXXXXXX)
```

### 7.3 Checklist final pré-submissão

**Instrução para Claude Code:**
```
Verifique o manuscrito SPYN_JCheminformatics.docx contra a checklist 
oficial do Journal of Cheminformatics e produza um relatório de conformidade.

Checklist JCheminformatics:
□ Abstract ≤ 350 palavras — VERIFICAR contagem
□ Keywords: 3–10 termos — VERIFICAR
□ Seção Background justifica a necessidade do software
□ Seção Implementation descreve linguagem, dependências, arquitetura
□ Seção Features descreve cada funcionalidade com figura
□ Seção Availability and Requirements completa (tabela padrão)
□ Comparação com softwares relacionados presente
□ Todos os dados do paper são reprodutíveis por terceiros
□ Software disponível sob licença OSI-approved
□ DOI Zenodo presente e funcional
□ CI badge presente (GitHub Actions ou equivalente)
□ Nenhuma figura > 150 dpi para submissão (ajustar se necessário)
□ Formato de referências: Vancouver (números entre colchetes)
□ Acknowledgements inclui financiadores com números de grant
□ Authors' contributions declaradas
□ Competing interests declarados

Para cada item: ✅ Conforme / ⚠️ Ajuste necessário / ❌ Faltando
```

---

## Resumo de prioridades por revista-alvo

### Journal of Cheminformatics (IF 5.7) — todos os itens são necessários

| Fase | Item | Prioridade |
|---|---|---|
| 3 | Testes automatizados | 🔴 Crítico |
| 3 | GitHub Actions CI | 🔴 Crítico |
| 5 | Comparação com CCP-NC / magresview | 🔴 Crítico |
| 2 | Reprodutibilidade (conda + exemplo) | 🟠 Alta |
| 4 | README e docs completos | 🟠 Alta |
| 6 | Zenodo v2 com metadados | 🟡 Média |
| 1 | Reestruturação do pacote | 🟡 Média |

### SoftwareX (IF 2.7) — conjunto mínimo viável

| Fase | Item | Prioridade |
|---|---|---|
| 1 | README completo | 🔴 Crítico |
| 2 | Exemplo reprodutível (sem QE) | 🔴 Crítico |
| 6 | Zenodo v2 com metadados | 🔴 Crítico |
| 3 | Testes mínimos (≥ Boltzmann + Lorentz) | 🟠 Alta |
| 4 | docs/installation.md | 🟠 Alta |
| 5 | Comparação (pode ser só tabela) | 🟡 Média |

### JOSS (IF 2.4, APC $0) — conjunto mínimo viável

| Fase | Item | Prioridade |
|---|---|---|
| 3 | Testes automatizados (todos os 4 módulos) | 🔴 Crítico |
| 3 | GitHub Actions CI | 🔴 Crítico |
| 2 | Exemplo reprodutível | 🔴 Crítico |
| 4 | README + docs/installation.md | 🔴 Crítico |
| 6 | Zenodo v2 | 🟠 Alta |
| 1 | Reestruturação (setup.py/pyproject.toml) | 🟠 Alta |

---

## Comandos de referência rápida para Claude Code

```bash
# Clonar o repositório
git clone https://github.com/jeffrichardchemistry/spyn.git
cd spyn

# Verificar estrutura atual
find . -name "*.py" | sort
find . -name "*.sh" | sort

# Instalar em modo desenvolvimento
pip install -e .

# Rodar testes (após Fase 3)
pytest tests/ -v --cov=spyn

# Gerar relatório de cobertura HTML
pytest tests/ --cov=spyn --cov-report=html
open htmlcov/index.html

# Verificar se o exemplo reprodutível funciona
cd examples/lamivudine
python run_example.py
ls -la example_spectrum.png   # deve existir após execução

# Criar release e tag (após todas as fases)
git tag -a v2.0.0 -m "Version 2.0.0 — publication-ready release"
git push origin v2.0.0
# → dispara integração Zenodo automaticamente (se configurada)
```

---

## Referências dos critérios utilizados

- Journal of Cheminformatics — Author Instructions: https://jcheminf.biomedcentral.com/submission-guidelines
- SoftwareX — Guide for Authors: https://www.sciencedirect.com/journal/softwarex/about/guide-for-authors
- JOSS — Review criteria: https://joss.readthedocs.io/en/latest/reviewer_guidelines.html
- SPYN v1.0.0 Zenodo: https://doi.org/10.5281/zenodo.4019024
- SPYN GitHub: https://github.com/jeffrichardchemistry/spyn

---

*Pipeline gerado com base na avaliação crítica de publicabilidade do SPYN — LACIQ/UFG, março de 2026*
