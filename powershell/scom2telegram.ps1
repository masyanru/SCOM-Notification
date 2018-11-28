Param (
[String]$AlertName,
[String]$AlertDescription,
[String]$AlertSource,
[String]$AlertTime,
[String]$parse_mode = "Markdown"
)

#Токен бота
$token = "123укцапи546н34543253"
#ID чата, группы или лички
$сhatid = "-п435е54р56евапрвп"

$Message = $AlertName + "`n" +  "`n"  + $AlertDescription + "`n" + $AlertSource + "`n" + $AlertTime

#Тип данных Markdown
$payload = @{ "parse_mode" = $parse_mode; "disable_web_page_preview" = "True" }
#
$URL = "https://api.telegram.org/bot$token/sendMessage?chat_id=$сhatid&text=$Message"
#или proxy https://habr.com/post/424427/
#
$request = Invoke-WebRequest -Uri $URL -Method Post `
                              -ContentType "application/json; charset=utf-8" `
                              -Body (ConvertTo-Json -Compress -InputObject $payload)