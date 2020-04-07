import re

a = [
    'http://fitgirl-repacks.site/all-my-repacks-a-z/', 'http://fitgirl-repacks.site/faq/',
    'http://fitgirl-repacks.site/donations/', 'http://fitgirl-repacks.site/donate-by-mining/',
    'http://fitgirl-repacks.site/contacts/', 'http://fitgirl-repacks.site/repacks-troubleshooting/',
    'http://1337x.to/torrent/3208218/303-Squadron-Battle-of-Britain-MULTi7-FitGirl-Repack/',
    'magnet:?xt=urn:btih:A68B1757CFA2616E14DA7669604ACCD42DDC4E42', 'http://sendfile.su/1439519',
    'http://rutor.info/torrent/650967/303-squadron-battle-of-britain-2018-pc-repack-ot-fitgirl',
    'magnet:?xt=urn:btih:c951c5f07c249926227072b91daddfe3a2365939&dn=rutor.info_303+Squadron%3A+Battle+of+Britain+%282018%29+PC+%7C+Repack+%D0%BE%D1%82+FitGirl&tr=udp://opentor.org:2710&tr=udp://opentor.org:2710&tr=http://retracker.local/announce',
    'http://tapochek.net/viewtopic.php?p=2528483', 'https://paste2.org/2VceCCE6', 'http://jdownloader.org/jdownloader2',
    'https://scenegames.goodolddownloads.com/release/303.Squadron.Battle.of.Britain-FitGirl/',
    'https://public.upera.co/f/aToI7sf5', 'http://fitgirl-repacks.site/all-my-repacks-a-z/',
    'http://fitgirl-repacks.site/faq/', 'http://fitgirl-repacks.site/donations/',
    'http://fitgirl-repacks.site/donate-by-mining/', 'http://fitgirl-repacks.site/contacts/',
    'http://fitgirl-repacks.site/repacks-troubleshooting/', 'http://fitgirl-repacks.site/2019/02/',
    'http://fitgirl-repacks.site/2019/01/', 'http://fitgirl-repacks.site/2018/12/',
    'http://fitgirl-repacks.site/2018/11/', 'http://fitgirl-repacks.site/2018/10/',
    'http://fitgirl-repacks.site/2018/09/', 'http://fitgirl-repacks.site/2018/08/',
    'http://fitgirl-repacks.site/2018/07/', 'http://fitgirl-repacks.site/2018/06/',
    'http://fitgirl-repacks.site/2018/05/', 'http://fitgirl-repacks.site/2018/04/',
    'http://fitgirl-repacks.site/2018/03/', 'http://fitgirl-repacks.site/2018/02/',
    'http://fitgirl-repacks.site/2018/01/', 'http://fitgirl-repacks.site/2017/12/',
    'http://fitgirl-repacks.site/2017/11/', 'http://fitgirl-repacks.site/2017/10/',
    'http://fitgirl-repacks.site/2017/09/', 'http://fitgirl-repacks.site/2017/08/',
    'http://fitgirl-repacks.site/2017/07/', 'http://fitgirl-repacks.site/2017/06/',
    'http://fitgirl-repacks.site/2017/05/', 'http://fitgirl-repacks.site/2017/04/',
    'http://fitgirl-repacks.site/2017/03/', 'http://fitgirl-repacks.site/2017/02/',
    'http://fitgirl-repacks.site/2017/01/', 'http://fitgirl-repacks.site/2016/12/',
    'http://fitgirl-repacks.site/2016/11/', 'http://fitgirl-repacks.site/2016/10/',
    'http://fitgirl-repacks.site/2016/09/', 'http://fitgirl-repacks.site/2016/08/',
    'http://fitgirl-repacks.site/2016/07/'
]
l='magnet:?xt=urn:btih:'
for each in a:
    match = re.match('magnet:\?xt=urn:btih:[\d|a-z|A-Z]+$', each)
    if match:
        print(match.group())
