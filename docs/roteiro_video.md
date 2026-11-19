# Roteiro do vídeo técnico (máximo 3 minutos)

Publicar no YouTube como **não listado**. Meta de duração: entre 2:30 e 2:50, para sobrar margem dos 3:00.

Antes de gravar: aumente a fonte do terminal, rode `python main.py --demo` uma vez para conferir e use a mesma tela do assistente que o grupo vai entregar.

| Tempo | Tela | Narração |
|---|---|---|
| 0:00 a 0:15 | Slide ou README com o título | "Nesta Global Solution, o Citizen Assist AI ganhou um módulo de energia. O público são famílias que querem entender e reduzir a conta de luz, que subiu em 2026." |
| 0:15 a 0:45 | Terminal: pergunta "Quanto minha casa consome?" e a tabela de consumo | "Usamos uma casa exemplo de três pessoas, com dados estimados e identificados no repositório. Energia é potência vezes tempo: o chuveiro, de 5.500 watts, ligado 24 minutos por dia, gasta 66 quilowatts-hora por mês. No total a casa consome 194 quilowatts-hora, cerca de 209 reais, usando a tarifa média da ANEEL mais tributos. O chuveiro é 34% do consumo e a geladeira, 20%." |
| 0:45 a 1:30 | Terminal: "Como reduzir minha conta de luz?" e a tabela de comparação | "Para o mesmo problema, reduzir a conta, comparamos duas alternativas. A primeira é trocar dez lâmpadas fluorescentes por LED: custa 60 reais, economiza 9 quilowatts-hora por mês e se paga em cerca de seis meses. A segunda é energia solar, nossa fonte renovável: três módulos, 1,65 quilowatt-pico, 4.686 reais. Gera 173 quilowatts-hora por mês e economiza entre 128 e 137 reais por mês, com retorno de cerca de três anos. Essa economia cai com o Fio B da Lei 14.300, que chega a 90% em 2028. Em CO2 os dois ganhos são pequenos, porque a rede brasileira já emite pouco." |
| 1:30 a 2:15 | Terminal: pergunta "vale a pena colocar painel solar?", depois menu opção 3 com 1500 W, 2 h, Enter | "Agora, no assistente. Pergunto se vale a pena colocar painel solar. Ele responde com o cálculo passo a passo, o custo, o retorno nos dois cenários e termina com as fontes e as limitações. No menu, a opção 3 calcula qualquer aparelho: informo 1.500 watts por duas horas por dia e ele devolve 90 quilowatts-hora, o custo em reais e o CO2. O usuário também pode digitar a tarifa da própria fatura." |
| 2:15 a 2:40 | Tela com a linha "Atenção" da resposta ou slide de recomendações | "Nossa recomendação é começar pelo LED, que é barato e rápido, e considerar o solar quando há imóvel próprio e consumo alto. Lembrando: são estimativas, não garantias. Usamos preços de 2025 e 2026, e o resultado muda com a tarifa, o telhado e as regras da ANEEL." |
| 2:40 a 2:50 | README no GitHub | "O código, os dados, os cálculos e as referências estão no repositório do GitHub, com o link na descrição. Obrigado!" |

## O que o vídeo precisa mostrar (conferência)

- [ ] O público e a necessidade energética escolhida
- [ ] A análise de consumo e a comparação das alternativas, incluindo a fonte renovável
- [ ] Uma demonstração das funcionalidades de energia no assistente
- [ ] As principais recomendações e as limitações
