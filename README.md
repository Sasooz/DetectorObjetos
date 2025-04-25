# Configuração do Projeto para Windows

## Passos para Clonar e Configurar o Repositório

### 1. **Instalar o Git LFS**

Antes de clonar o repositório, você precisa instalar o Git LFS para gerenciar arquivos grandes (como o modelo `yolov5l.pt`).

- Acesse o [site oficial do Git LFS](https://git-lfs.github.com/) e baixe o instalador para Windows.
- Execute o instalador e siga as instruções para completar a instalação.
- Após a instalação, configure o Git LFS com o comando:

```bash
git lfs install

# Clone o Repositório

# Verifique o download dos arquivos grandes

```bash
git lfs ls-files

# Instale as depêndencias do projeto

```bash
pip install -r requirements.txt
