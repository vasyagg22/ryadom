#!/usr/bin/env python3
"""Private-by-default experimental MIT PocketPal v1.24.0 fork called Два ИИ."""
from pathlib import Path
import json
from PIL import Image, ImageDraw

root=Path("pocketpal")
assert (root/"LICENSE").is_file()
p=json.loads((root/"package.json").read_text())
assert p.get("version")=="1.24.0", "Unexpected PocketPal revision"

def replace(path,old,new):
    f=root/path
    t=f.read_text()
    assert t.count(old)==1, (path,old,t.count(old))
    f.write_text(t.replace(old,new,1))
replace("android/app/build.gradle",'applicationId "com.pocketpalai"','applicationId "app.duo.offlineai"')
replace("android/app/build.gradle",'versionName "1.24.0"','versionName "0.1.0"')
replace("android/app/build.gradle",'versionCode 161','versionCode 1')
replace("android/app/build.gradle",'apply plugin: "com.google.gms.google-services"','// Standalone app: no Firebase Google Services plugin')
replace("android/app/src/main/res/values/strings.xml",'<string name="app_name">PocketPal</string>','<string name="app_name">Два ИИ</string>')
replace("android/app/src/main/AndroidManifest.xml",'android:scheme="pocketpal"','android:scheme="duoai"')
app=root/"app.json"
obj=json.loads(app.read_text())
obj["displayName"]="Два ИИ"
app.write_text(json.dumps(obj,ensure_ascii=False,indent=2))
(root/".env").write_text("ENABLE_PALSHUB_INTEGRATION=false\nENABLE_AUTHENTICATION=false\nENABLE_OFFLINE_MODE=true\nAPP_URL=duoai://app\n")
g=root/"android/app/google-services.json"
if g.exists():g.unlink()

palette={
"const LIGHT_PRIMARY = '#333333';":"const LIGHT_PRIMARY = '#33234E';",
"const LIGHT_SECONDARY = '#1E4DF6';":"const LIGHT_SECONDARY = '#6945D8';",
"const LIGHT_TERTIARY = '#7880FF';":"const LIGHT_TERTIARY = '#9B80EB';",
"const LIGHT_BACKGROUND = '#ffffff';":"const LIGHT_BACKGROUND = '#F8F7FF';",
"const LIGHT_SURFACE = '#F9FAFB';":"const LIGHT_SURFACE = '#FFFFFF';",
"const DARK_PRIMARY = '#DADDE6';":"const DARK_PRIMARY = '#F1EAFF';",
"const DARK_SECONDARY = '#95ABE6';":"const DARK_SECONDARY = '#A78BFA';",
"const DARK_TERTIARY = '#80E6E4';":"const DARK_TERTIARY = '#C8B7FF';",
"const DARK_BACKGROUND = '#000000';":"const DARK_BACKGROUND = '#121020';",
"const DARK_SURFACE = '#0E0E0E';":"const DARK_SURFACE = '#1A172A';",
"  authorBubbleBackground: '#f2f2f2',":"  authorBubbleBackground: '#EEE9FC',",
"  authorBubbleBackground: '#212121',":"  authorBubbleBackground: '#29213D',"
}
for a,b in palette.items():replace("src/theme/tokens/colors.ts",a,b)
input_styles=[
("      borderRadius: 12,\n      overflow: 'hidden',","      borderRadius: 20,\n      overflow: 'hidden',"),
("      paddingHorizontal: 24,\n      paddingTop: 20,\n      paddingBottom: 8,","      paddingHorizontal: 18,\n      paddingTop: 14,\n      paddingBottom: 8,"),
("      paddingHorizontal: 24,\n      paddingVertical: 10,","      paddingHorizontal: 18,\n      paddingVertical: 8,"),
("      paddingHorizontal: 24,\n      paddingVertical: 20,","      paddingHorizontal: 18,\n      paddingVertical: 14,")]
for a,b in input_styles:replace("src/components/ChatInput/styles.ts",a,b)
file="src/screens/ChatScreen/ChatScreen.tsx"
replace(file,"import {StyleSheet, View} from 'react-native';","import {StyleSheet, View, Text} from 'react-native';")
replace(file,"        <ChatView\n", """        <View style={styles.duoBar} accessible accessibilityRole="summary">
          <View style={styles.duoDot} />
          <Text style={styles.duoModel} numberOfLines={1}>
            {'Два ИИ  ·  ' + (modelStore.activeModel?.name ?? 'Выберите GGUF-модель')}
          </Text>
          <Text style={styles.duoVision}>
            {visionEnabled ? 'ФОТО ✓' : 'ТЕКСТ'}
          </Text>
        </View>
        <ChatView
""")
replace(file,"""const styles = StyleSheet.create({
  chat: {
    flex: 1,
  },
});""","""const styles = StyleSheet.create({
  chat: {flex: 1},
  duoBar: {
    height: 39, marginHorizontal: 12, marginTop: 7, marginBottom: 2,
    paddingHorizontal: 12, backgroundColor: '#251A40',
    borderColor: '#40325E', borderWidth: 1, borderRadius: 14,
    flexDirection: 'row', alignItems: 'center',
  },
  duoDot: {width: 7, height: 7, borderRadius: 4, backgroundColor: '#BCA7FF', marginRight: 8},
  duoModel: {flex: 1, fontSize: 12, fontWeight: '600', color: '#F9F6FF'},
  duoVision: {marginLeft: 7, fontSize: 9, fontWeight: '700', letterSpacing: 0.5, color: '#D9CCFA'},
});""")
locale=root/"src/locales/ru.json"
o=json.loads(locale.read_text())
o["chat"]["modelNotLoaded"]="Добавьте и загрузите GGUF-модель"
o["about"]["description"]="Два ИИ — локальный помощник на базе PocketPal AI (MIT) и llama.cpp."
o["about"]["supportProjectDescription"]="Открытый PocketPal AI: поддержать создателей оригинала:"
locale.write_text(json.dumps(o,ensure_ascii=False,indent=2)+"\n")

res=root/"android/app/src/main/res"
fg=res/"drawable/ic_launcher_foreground.xml"
fg.write_text('''<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">
<path android:pathData="M52,54 C43,40 29,45 31,56 C33,71 48,68 55,54 C64,40 78,43 79,55 C79,71 65,67 56,57"
android:fillColor="@android:color/transparent" android:strokeColor="#CBB9FF"
android:strokeWidth="7" android:strokeLineCap="round" android:strokeLineJoin="round"/>
<path android:fillColor="#FFFFFF" android:pathData="M79,29 a5,5 0,1 0,0 10 a5,5 0,1 0,0 -10"/>
</vector>''')
mono=res/"drawable/ic_launcher_monochrome.xml"
mono.write_text(fg.read_text().replace('#CBB9FF','#FFFFFF'))
(res/"values/ic_launcher_background.xml").write_text('<?xml version="1.0" encoding="utf-8"?><resources><color name="ic_launcher_background">#201538</color></resources>')
for density,size in [("mdpi",48),("hdpi",72),("xhdpi",96),("xxhdpi",144),("xxxhdpi",192)]:
    n=size*4
    pic=Image.new("RGBA",(n,n),"#201538")
    d=ImageDraw.Draw(pic)
    line=round(n*.066)
    d.arc([n*.145,n*.27,n*.57,n*.73],65,305,fill="#CBB9FF",width=line)
    d.arc([n*.43,n*.27,n*.855,n*.73],245,485,fill="#F4EBFF",width=line)
    d.ellipse([n*.725,n*.20,n*.805,n*.28],fill="#FFFFFF")
    pic=pic.resize((size,size),Image.Resampling.LANCZOS)
    for name in ["ic_launcher.png","ic_launcher_round.png"]:
        pic.save(res/f"mipmap-{density}"/name)

(root/"DOWNSTREAM-NOTICE.txt").write_text("Два ИИ: experimental MIT fork of PocketPal AI v1.24.0.\nhttps://github.com/a-ghorbani/pocketpal-ai\nOriginal LICENSE preserved. Not affiliated with PocketPal.\n")
print("PATCH_OK app.duo.offlineai Два ИИ")
