#bot1
import asyncio
import aiohttp
import io
import discord
from discord.ext import commands
from collections import deque
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# CONFIGURAÇÕES
ID_DO_SERVIDOR = 1361898946867237125  # 🟡 Substitua pelo ID do seu servidor SSP - GUARUJÁ RP
ID_DO_CARGO_MENSAGEM = 1364016462154563614  # Cargo que pode usar /mensagem PRESIDENTE
ID_DO_CARGO_MENSAGEM = 1364016541330575451  # Cargo que pode usar /mensagem V. PRESIDENTE
ID_DO_CARGO_MENSAGEM = 1389710649390534717  # Cargo que pode usar /mensagem GOVERNADOR
ID_DO_CARGO_MENSAGEM = 1376730670910537788  # Cargo que pode usar /mensagem DEV
ID_DO_CARGO_PERMITIDO = 1377464656657907793 # Cargo que pode usar giverole/removerole/painel ⭐ |  Administrativo
ID_CANAL_LOGS = 1390749263478128700  # Canal onde logs serão enviados 〘📑〙ʀʜ-ʀᴇɢɪꜱᴛʀᴏ

CARGOS_AUTORIZADOS = [
    1363298591614963772,  # Novato
    1362608768189468732,  # EM/PM
    1362605324615549119,  # Comandante Geral
    1362602352368029706,  # Subcomandante Geral
    1362609132716167279,  # ❖  | Quartel Comando Geral
    1362609058057687080,  # ❖ | CoordOp QCG
    1377457842943955034,  # [QOPM] Quadro de Oficiais da Policia Militar
    1377458004328321124,  # [QPES] Quadro de Praças Especiais da Policia Militar
    1377458150566793336,  # [QPPM] Quadro de Praças da Policia Militar
    1362602023488323676,  # [Oficiais Superiores]
    1362602046330769468,  # [Oficiais intermediários]
    1362602115712942152,  # [Praças Graduados]
    1362602151435702393,  # [Praças]
    1362602399189172244,  # Coronel PM
    1362602485092581586,  # Tenente Coronel PM
    1362602512120549499,  # Major PM
    1362602545897537768,  # Capitão PM
    1362602576419360778,  # 1º Tenente PM
    1362602616348999781,  # 2º Tenente PM
    1362602649307844838,  # Aspirante a Oficial PM
    1362602675312787526,  # Sub-Tenente PM
    1362602703707963484,  # 1º Sargento PM
    1362602740160790599,  # 2º Sargento PM
    1362602768732393503,  # 3º Sargento PM
    1362602794338746418,  # ◊❯❯  |  Aluno ESSg
    1362602838928134345,  # Cabo PM
    1362602865285140490,  # Soldado de 1º Classe PM
    1362602895391981689,  # Soldado de 2º Classe PM
    1377464656657907793,  # ⭐ |  Administrativo
    1376346261489188944,  # Corregedor Geral
    1390774259194007726,  # Subcorregedor Geral
    1390791950877196288,  # Corregedor
    1390792374296248511,  # 👮  | Estagiário DPM
    1376724464846241823,  # 👮  | Braçal de DPM
    1368694431946903744,  # DPM - CORREGEDORIA MILITAR
    1376346868707229877,  # 👮‍♂️ | COMANDANTE CAvPM
    1376347005244149821,  # 👮‍♂️ | SUB COMANDANTE CAvPM
    1368695624517681324,  # 👮‍♂️ | CAvPM
    1376349679423459378,  # Comandante 21° BPM/M
    1376349815168045146,  # Subcomandante 21° BPM/M
    1376349149791785091,  # 21° BPM
    1376349238044393612,  # 1° CIA
    1376352696977850418,  # Comandante FT
    1376352732931428482,  # Subcomandante FT
    1376352775016939550,  # 𝐅𝐓  | Braçal Força Tática
    1368751842972139601,  # 𝐅𝐓  | Estagiário Força Tática
    1376353262390874263,  # FORÇA TÁTICA  
    1376350712816074804,  # Comandante BAEP     
    1376350151907741708,  # Subcomandante BAEP     
    1376724288219910306,  # ⚡  | Braçal de BAEP     
    1377460615333019648,  # ⚡ | Estagiário Baep    
    1368752196052582442,  # BAEP     
    1376726705611345970,  # Comandante 1°BpChq     
    1376726761294925897,  # Subcomandante 1°BpChq     
    1362613997467074661,  # ⚡  | Braçal de ROTA     
    1362615152675000381,  # ⚡ | Estagiário ROTA 
    1362613766176505916,  # ROTA         
    1376351189435682856,  # Comandante 2°BpChq     
    1376351021311459448,  # Subcomandante 2°BpChq     
    1376352139990929550,  # ⚡| Braçal ROCAM     
    1376351820590612500,  # ⚡| Estagiário ANCHIETA
    1368752340450017341,  # ANCHIETA         
    1376351246562099321,  #  Comandante 3°BpChq    
    1376351123488637008,  #  Subcomandante 3°BpChq    
    1376351837212639332,  #  ⚡| Estagiário Humaitá    
    1368752343679762452,  #  HUMAITÁ    
    1376351283795202128,  #  Comandante 4°BpChq    
    1376351161451413525,  #  Subcomandante 4°BpChq    
    1376351871786291311,  #  ⚡| Estagiário  COE    
    1377826439004553216,  #  [ COESp ]    
    1368752346015862855,  #  COE    
    1389772575932158002,  #  🔵 | Terceira Classe    
    1389772623621394524,  #  🔵 | Segunda Classe    
    1389772644135731402,  #  🔵 | Primeira Classe    
    1389772671876862093,  #  🔵 | Classe Especial   
    1389772697038491689,  #  🔵 | Inspetor de Terceira Classe
    1389772714255974570,  #  🔵 | Inspetor de Segunda Classe
    1389772739983835176,  #  🔵 | Inspetor de Primeira Classe
    1390450091869077564,  #  🔵 | GCM
    1368060540483538954,  #  👨‍✈️ | Delegado Geral
    1368060484695228477,  #  👨‍✈️ | Chefe de Polícia
    1368060423370309704,  #  👨‍✈️ | Delegado Adjunto
    1368061324562792528,  #  👨‍✈️ | Perito Técnico
    1368060367280017489,  #  👨‍✈️ | Perito Criminal
    1368060294689194024,  #  👨‍✈️ | Delegado de Polícia
    1368060090439045160,  #  👨‍✈️ | Investigador de Polícia
    1368059603241406484,  #  👨‍✈️ | Escrivão de Polícia
    1362605219711549481,  #  🩸 │APH Tático
    1362609893286219968,  #  🔵 |  Academia do Barro Branco
    1362605360153628722,  #  (CFSd) - Curso de Formaçâo de Soldados  
    1362605421109711012,  #  (CSP) - Curso Superior de Policia
    1362605441477251192,  #  (CAO) - Curso de Aperfeiçoamento de Oficiais
    1362605492865863750,  #  (CAS) Curso de Aperfoiçoamento de Sargentos
    1362605547614109716,  #  📃 | Curso P.O.P
    1362605601317851287,  #  📃 | Curso Abordagem e Posicionamento
    1362605589531722070,  #  📃 | Curso Modulaçâo e BOPM  
    1362605629008515213,  #  🛵 │SAT A
    1362605661896183988,  #  🚓 │SAT B
    1362605740858015844,  #  🎯 │Curso Tiro Avançado
    1362605984496750592,  #  🎯 │Curso Tiro Básico
    1362610928977445058,  #  🎯 | Curso de Ações
    1362606088482066462,  #  CFO │Curso de Formação de Oficiais
    1362606602263199955,  #  CAS │Curso de Aperfeiçoamento de Sargentos
    1362606645556805642,  #  CFS │Curso de Formação de Sargentos
    1362606692696723591,  #  CFC │Curso de Formação de Cabos
    1362606731271606413,  #  CFAP │Centro de Formação e Aperfeiçoamento de Praças
    1362609213834137844,  #  📆 | CPC
    1362611122942902312,  #  📃 | LET - Legislação Especifica de Trânsito
    1362611450266386502,  #  🚓 |  Curso de Direção Defensiva
    1362611615052071123,  #  🦅 | Curso de Gerenciamento de Crises
    1362611794614423562,  #  📃 | Curso de Direito Penal       
    1362602084477702224,  #  👮‍♂️ | Policia Militar
    1368759311316291664,  #  👨‍✈️ |  Policia Civil
    1389767734220554250,  #  👮‍♂️ | Guarda Civil Metropolitana
]

# Memória temporária para registrar últimos logs
ULTIMOS_LOGS = deque(maxlen=10)

@bot.tree.command(name="mensagem", description="Envie uma mensagem pelo bot", guild=discord.Object(id=ID_DO_SERVIDOR))
async def mensagem(interaction: discord.Interaction):
    if not any(discord.utils.get(interaction.user.roles, id=role_id) for role_id in [
        1364016462154563614,  # PRESIDENTE
        1364016541330575451,  # VICE PRESIDENTE
        1389710649390534717,  # GOVERNADOR
        1376730670910537788   # DEV
    ]):
        await interaction.response.send_message("❌ Você não tem permissão para usar este comando.", ephemeral=True)
        return

    class MensagemModal(discord.ui.Modal, title="📨 Enviar Mensagem"):
        conteudo = discord.ui.TextInput(
            label="Conteúdo da Mensagem",
            style=discord.TextStyle.paragraph,
            placeholder="Escreva a mensagem com quebras de linha, emojis etc.",
            max_length=2000
        )

        async def on_submit(self, interaction_modal: discord.Interaction):
            await interaction_modal.response.send_message("⏳ Enviando mensagem...", ephemeral=True)
            sent_msg = await interaction.channel.send(self.conteudo.value)

            await interaction_modal.followup.send(
                "📎 Se desejar, **responda à mensagem enviada** com anexos (imagens/vídeos) **em até 5 minutos**.",
                ephemeral=True
            )

            def check(m):
                return (
                    m.reference and
                    m.reference.message_id == sent_msg.id and
                    m.author == interaction_modal.user and
                    m.channel == interaction_modal.channel
                )

            try:
                reply_msg = await bot.wait_for("message", timeout=300.0, check=check)

                arquivos = []
                async with aiohttp.ClientSession() as session:
                    for attachment in reply_msg.attachments:
                        async with session.get(attachment.url) as resp:
                            if resp.status == 200:
                                data = await resp.read()
                                arquivos.append(discord.File(fp=io.BytesIO(data), filename=attachment.filename))

                try:
                    await sent_msg.delete()
                except discord.Forbidden:
                    pass
                try:
                    await reply_msg.delete()
                except discord.Forbidden:
                    pass

                await interaction.channel.send(content=self.conteudo.value, files=arquivos)

            except asyncio.TimeoutError:
                pass

    await interaction.response.send_modal(MensagemModal())

# COMANDO /giverole
@bot.tree.command(name="giverole", description="Atribui um cargo a um membro", guild=discord.Object(id=ID_DO_SERVIDOR))
async def giverole(interaction: discord.Interaction, membro: discord.Member, cargo: discord.Role):
    if not discord.utils.get(interaction.user.roles, id=ID_DO_CARGO_PERMITIDO):
        await interaction.response.send_message("❌ Você não tem permissão para usar este comando.", ephemeral=True)
        return

    if cargo.id not in CARGOS_AUTORIZADOS:
        await interaction.response.send_message("❌ Este cargo não está autorizado.", ephemeral=True)
        return

    try:
        await membro.add_roles(cargo)

        embed = discord.Embed(
            title="✅ Cargo Atribuído",
            description=f"O cargo **{cargo.name}** foi atribuído a {membro.mention}.",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Por: {interaction.user}", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

        # Salvar log
        ULTIMOS_LOGS.appendleft({
            "executor": interaction.user,
            "alvo": membro,
            "cargo": cargo.name,
            "acao": "adicionou",
            "hora": discord.utils.utcnow()
        })

        # Log no canal
        canal_logs = bot.get_channel(ID_CANAL_LOGS)
        if canal_logs:
            embed = discord.Embed(
                title="📌 Cargo Atribuído",
                description=f"**{interaction.user.mention}** atribuiu o cargo **{cargo.name}** para {membro.mention}",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            )
            embed.set_footer(text=f"ID: {membro.id}")
            await canal_logs.send(embed=embed)

    except discord.Forbidden:
        await interaction.response.send_message("❌ Permissão insuficiente do bot.", ephemeral=True)


# COMANDO /removerole
@bot.tree.command(name="removerole", description="Remove um cargo de um membro", guild=discord.Object(id=ID_DO_SERVIDOR))
async def removerole(interaction: discord.Interaction, membro: discord.Member, cargo: discord.Role):
    if not discord.utils.get(interaction.user.roles, id=ID_DO_CARGO_PERMITIDO):
        await interaction.response.send_message("❌ Você não tem permissão para usar este comando.", ephemeral=True)
        return

    if cargo.id not in CARGOS_AUTORIZADOS:
        await interaction.response.send_message("❌ Este cargo não está autorizado.", ephemeral=True)
        return

    try:
        await membro.remove_roles(cargo)

        embed = discord.Embed(
            title="🚫 Cargo Removido",
            description=f"O cargo **{cargo.name}** foi removido de {membro.mention}.",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Por: {interaction.user}", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

        # Salvar log
        ULTIMOS_LOGS.appendleft({
            "executor": interaction.user,
            "alvo": membro,
            "cargo": cargo.name,
            "acao": "removeu",
            "hora": discord.utils.utcnow()
        })

        # Log no canal
        canal_logs = bot.get_channel(ID_CANAL_LOGS)
        if canal_logs:
            log_embed = discord.Embed(
                title="📌 Cargo Removido",
                description=f"**{interaction.user.mention}** removeu o cargo **{cargo.name}** de {membro.mention}",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            )
            log_embed.set_footer(text=f"ID: {membro.id}")
            await canal_logs.send(embed=log_embed)

    except discord.Forbidden:
        await interaction.response.send_message("❌ Permissão insuficiente do bot.", ephemeral=True)

# COMANDO /painel
# COMANDO /painel
@bot.tree.command(name="painel", description="Exibe painel de controle do sistema de cargos", guild=discord.Object(id=ID_DO_SERVIDOR))
async def painel(interaction: discord.Interaction):
    if not discord.utils.get(interaction.user.roles, id=ID_DO_CARGO_PERMITIDO):
        await interaction.response.send_message("❌ Você não tem permissão para ver o painel.", ephemeral=True)
        return

    embed = discord.Embed(
        title="📊 Painel de Controle - Cargos",
        color=discord.Color.blurple()
    )

    # Lista de cargos autorizados (dividido em blocos de até 1024 caracteres)
    cargos_texto = ""
    blocos = []

    for cargo_id in CARGOS_AUTORIZADOS:
        cargo_obj = interaction.guild.get_role(cargo_id)
        nome = cargo_obj.name if cargo_obj else f"❌ Cargo não encontrado ({cargo_id})"
        linha = f"- {nome} (`{cargo_id}`)\n"

        if len(cargos_texto) + len(linha) > 1024:
            blocos.append(cargos_texto)
            cargos_texto = ""
        cargos_texto += linha
    blocos.append(cargos_texto)

    for i, bloco in enumerate(blocos):
        embed.add_field(
            name=f"✅ Cargos Autorizados" + (f" (parte {i+1})" if len(blocos) > 1 else ""),
            value=bloco,
            inline=False
        )

    # Últimos logs
    if ULTIMOS_LOGS:
        historico = ""
        for log in ULTIMOS_LOGS:
            historico += (
                f"{log['executor'].mention} **{log['acao']}** `{log['cargo']}` "
                f"{'para' if log['acao'] == 'adicionou' else 'de'} {log['alvo'].mention} — "
                f"<t:{int(log['hora'].timestamp())}:R>\n"
            )
    else:
        historico = "Nenhuma ação registrada."

    embed.add_field(name="📁 Últimas Ações", value=historico, inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)


# AO INICIAR
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=ID_DO_SERVIDOR))
        print(f"✅ {len(synced)} comando(s) sincronizado(s).")
    except Exception as e:
        print(f"❌ Erro ao sincronizar comandos: {e}")

# INICIAR O BOT
TOKEN = os.getenv("TOKEN")