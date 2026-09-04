"""
Servidor MCP (Model Context Protocol) para o ConsultaGmail.
Permite que o Hermes Agent (e outros clientes MCP) consultem e analisem e-mails do Gmail com Gemini AI.
"""
from mcp.server.fastmcp import FastMCP
import gmail_core

mcp = FastMCP("Gmail AI Analyzer")


@mcp.tool()
def listar_ultimos_emails(max_results: int = 10) -> str:
    """
    Lista os metadados (remetente, assunto, data e ID) dos e-mails mais recentes da caixa de entrada.
    Esta consulta é rápida e NÃO consome cotas da IA Gemini.
    
    Args:
        max_results: Quantidade de e-mails a retornar (padrão: 10)
    """
    try:
        service = gmail_core.autenticar_gmail()
        emails = gmail_core.listar_ultimos_emails_metadados(service, max_results=max_results)
        if not emails:
            return "Nenhum e-mail encontrado na caixa de entrada."

        resultado = [f"📧 Encontrados {len(emails)} e-mails na Inbox:\n"]
        for idx, email in enumerate(emails, 1):
            resultado.append(
                f"{idx}. [ID: {email['id']}] {email['assunto']}\n"
                f"   De: {email['remetente']}\n"
                f"   Data: {email['data']}\n"
            )
        return "\n".join(resultado)
    except Exception as e:
        return f"Erro ao listar e-mails do Gmail: {str(e)}"


@mcp.tool()
def analisar_caixa_entrada(
    max_emails: int = 10,
    excluir_spam: bool = False,
    excluir_irrelevantes: bool = False
) -> str:
    """
    Analisa os e-mails da caixa de entrada usando o Gemini 2.5 Flash AI.
    Classifica cada e-mail em IMPORTANTE, IRRELEVANTE ou SPAM e gera resumos detalhados.
    
    Args:
        max_emails: Quantidade de e-mails para analisar (padrão: 10, máximo: 500)
        excluir_spam: Se True, move e-mails classificados como SPAM para a lixeira automaticamente
        excluir_irrelevantes: Se True, move e-mails classificados como IRRELEVANTE para a lixeira automaticamente
    """
    try:
        service = gmail_core.autenticar_gmail()
        creds = gmail_core.configurar_gemini()

        dados = gmail_core.analisar_caixa_entrada_dados(
            service=service,
            creds=creds,
            max_emails=max_emails,
            excluir_spam=excluir_spam,
            excluir_irrelevantes=excluir_irrelevantes
        )

        if dados['status'] == 'caixa_vazia':
            return "Caixa de entrada está vazia!"

        relatorio = ["=================================================="]
        relatorio.append("🤖 RELATÓRIO DE ANÁLISE DE E-MAILS (GEMINI AI)")
        relatorio.append("==================================================\n")

        for idx, msg in enumerate(dados['mensagens'], 1):
            if msg['classificacao'] == 'IMPORTANTE':
                tag_class = "⭐ IMPORTANTE"
            elif msg['classificacao'] == 'SPAM':
                tag_class = "🚨 SPAM"
            else:
                tag_class = "📭 IRRELEVANTE"

            status_exc = " 🗑️ (Excluído)" if msg['excluido'] else ""

            relatorio.append(f"📨 {idx}. [ID: {msg['id']}] De: {msg['remetente']}")
            relatorio.append(f"   Assunto: {msg['assunto']}")
            relatorio.append(f"   Data: {msg['data']}")
            relatorio.append(f"   Classificação: {tag_class}{status_exc}")
            if msg['titulo_resumido']:
                relatorio.append(f"   📌 Título: {msg['titulo_resumido']}")
            if msg['resumo']:
                relatorio.append(f"   📝 Resumo:\n      {msg['resumo']}")
            relatorio.append("-" * 50)

        stats = dados['estatisticas']
        relatorio.append("\n📊 ESTATÍSTICAS DA ANÁLISE:")
        relatorio.append(f"- E-mails processados: {stats['processados']}")
        relatorio.append(f"- ⭐ Importantes: {stats['importantes']}")
        relatorio.append(f"- 📭 Irrelevantes: {stats['irrelevantes']}")
        relatorio.append(f"- 🚨 Spam: {stats['spam']}")
        if stats['excluidos'] > 0:
            relatorio.append(f"- 🗑️ Movidos para a lixeira: {stats['excluidos']}")

        if dados['status'] == 'quota_excedida':
            relatorio.append("\n⚠️ AVISO: A análise foi interrompida pois a quota da API Gemini foi atingida.")

        return "\n".join(relatorio)

    except Exception as e:
        return f"Erro ao analisar e-mails com Gemini: {str(e)}"


@mcp.tool()
def mover_email_para_lixeira(email_id: str) -> str:
    """
    Move um e-mail específico para a lixeira do Gmail a partir do seu ID de mensagem.
    
    Args:
        email_id: O identificador único da mensagem no Gmail (ex: '18f23a9b4c0d1234')
    """
    try:
        service = gmail_core.autenticar_gmail()
        sucesso = gmail_core.excluir_email(service, email_id)
        if sucesso:
            return f"✅ E-mail de ID '{email_id}' foi movido para a lixeira com sucesso!"
        else:
            return f"❌ Não foi possível mover o e-mail '{email_id}' para a lixeira."
    except Exception as e:
        return f"Erro ao mover e-mail para lixeira: {str(e)}"


if __name__ == "__main__":
    mcp.run()
