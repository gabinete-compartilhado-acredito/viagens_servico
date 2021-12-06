/*** Protótipo de query (ainda em construção) para buscar por afastamentos no DOU.
Note que abandonamos essa estratégia para utilizar no lugar os dados de viagens a serviço 
do Portal da Transparência ***/

DECLARE regex STRING DEFAULT r'(?i).{1,40}(?:autoriz(?:o\b|a\b|ar\b)|conced(?:o\b|er\b|e\b)).{1,40}afasta.{1,20}';
--DECLARE regex STRING DEFAULT r'(?i).{1,40}(?:autorização).{1,40}afasta.{1,20}';
DECLARE notregex STRING DEFAULT '(?i)tornar sem efeito';


SELECT 
identifica, orgao, data_pub, tipo_edicao, 
REGEXP_EXTRACT(IFNULL(clean_text, alltext), regex) AS trecho, 
IFNULL(clean_text, alltext) AS texto, 
url 
FROM `gabinete-compartilhado.views_publicos.br_imprensa_oficial_dou_2`
WHERE (REGEXP_CONTAINS(clean_text, regex) OR REGEXP_CONTAINS(alltext, regex))
AND NOT (REGEXP_CONTAINS(clean_text, notregex) OR REGEXP_CONTAINS(alltext, notregex))

ORDER BY RAND()
