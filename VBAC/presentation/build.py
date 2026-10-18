from pathlib import Path
import json, re, base64, subprocess

ROOT=Path(__file__).resolve().parent.parent
SRC=ROOT/'presentation'
output=ROOT/'VBAC_AI_Career_Studio_Presentation.html'
base=SRC/'base-style.css'
if not base.exists():
    original=output.read_text(encoding='utf-8-sig')
    base.write_text(re.search(r'<style>([\s\S]*?)</style>',original).group(1),encoding='utf-8')
certs=json.loads((SRC/'certificates.json').read_text(encoding='utf-8'))
shorts=['พื้นฐาน AI', 'Generative AI', 'AI ช่วยงานประจำวัน', 'AI ในที่ทำงาน', 'AI ทำคอนเทนต์']
summaries=['พื้นฐานแนวคิด AI ใช้ประกอบการทดลองแยกภาพในสัปดาห์ 2', 'พื้นฐาน Generative AI, LLM, การสั่งงาน และแนวคิด agent เชื่อมกับการเขียนโจทย์ในสัปดาห์ 3', 'การใช้ AI ช่วยงานประจำวัน เชื่อมกับการอ่านและสรุปเอกสารในสัปดาห์ 5', 'AI คืออะไร การทำงานกับ AI และข้อจำกัด เรียนให้ผ่านก่อนเริ่มงานการตลาด ตรวจหลักฐานสัปดาห์ 6 เชื่อมกับการใช้ AI ในงานสำนักงาน', 'การวางคอนเทนต์ บุคลิกแบรนด์ และเครื่องมือ AI เชื่อมกับภาพ เสียง และคลิปในสัปดาห์ 13 และ 14']
images={1:'cert-microsoft-ai-concepts.png',4:'cert-samsung-workplace.jpg',5:'cert-samsung-marketing.jpg'}
evidence=['หลักฐานจบโมดูลในบัญชีตนเอง และบันทึกสิ่งที่พบจากการทดสอบภาพ', 'หลักฐานจบโมดูล และการวิเคราะห์องค์ประกอบ ความสามารถ และข้อจำกัดของระบบ AI', 'หลักฐานจบโมดูล พร้อมคำตอบจากเอกสารที่ตรวจแหล่งที่มาแล้ว', 'ใบประกาศที่ได้รับจริง พร้อมบันทึกข้อจำกัดและสิ่งที่ต้องตรวจ ก่อนเริ่มงานการตลาดสัปดาห์ 13', 'ใบประกาศที่ได้รับจริง พร้อมบทและสื่อที่ผู้เรียนตรวจแก้เอง']
for c in certs:
    i=c['id']-1;c['short']=shorts[i];c['summary']=summaries[i];c['evidence']=evidence[i]
    if c['id']<=3:
        c['kind']='หลักฐานจบโมดูล / Achievement'
        c['condition']='เรียนและทำแบบประเมินตามเกณฑ์หน้าโมดูลด้วยตนเอง เข้าสู่ระบบเพื่อบันทึกผลในโปรไฟล์ เป็นหลักฐานการเรียน ไม่ใช่การสอบ Microsoft Certification'
    else:
        c['kind']='ใบประกาศเมื่อผ่านเกณฑ์'
        c['condition']='หน้ารายวิชาระบุว่าเรียนไม่มีค่าธรรมเนียมและได้รับ certificate เมื่อจบ มีแบบทดสอบรายบท ต้องตรวจเกณฑ์ผ่านและขั้นตอนรับเอกสารล่าสุดในบัญชี ผู้เรียนต้องเรียนและสอบด้วยตนเอง'
    if c['id'] in images:
        name=images[c['id']];b=(ROOT/'assets/certificates'/name).read_bytes()
        mime='image/png' if name.endswith('.png') else 'image/jpeg'
        c['image']='data:'+mime+';base64,'+base64.b64encode(b).decode()
        c['imageSource']='https://paphatchailab.github.io/AI-Consultant-Profile/image/'+name
    else:c['image']=None
logos=json.loads((ROOT/'assets/tool-logos.json').read_text(encoding='utf-8'))
assert all('src' in v for v in logos.values())
data=(SRC/'curriculum.js').read_text(encoding='utf-8')
ai_day=(ROOT/'assets/ai-day-exhibition.png').read_bytes()
visuals={'aiDay':'data:image/png;base64,'+base64.b64encode(ai_day).decode()}
script="'use strict';\nconst visuals="+json.dumps(visuals)+';\n'+data+'\nconst certs='+json.dumps(certs,ensure_ascii=False)+';\nconst logos='+json.dumps(logos,ensure_ascii=False)+';\n'+(SRC/'interactions.js').read_text(encoding='utf-8')
css=base.read_text(encoding='utf-8')+'\n'+(SRC/'roadmap.css').read_text(encoding='utf-8')
html='<!doctype html>\n<html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="หลักสูตร AI Native สำหรับทุกสาขา 16 สัปดาห์ พร้อม Paperless-ngx สื่อโฆษณา เว็บ Workflow และ AI Agent"><title>VBAC | AI NATIVE: THE NEXT WORKFORCE</title><style>'+css+'</style></head><body>\n'+(SRC/'page-body.html').read_text(encoding='utf-8')+'\n<script>'+script+'</script>\n</body></html>'
banner=(ROOT/'assets/ai-native-course-banner.png').read_bytes()
html=html.replace('__SHOP_BANNER__','data:image/png;base64,'+base64.b64encode(banner).decode())
output.write_text(html,encoding='utf-8')
(SRC/'certificates-public.json').write_text(json.dumps([{k:v for k,v in c.items() if k!='image'} for c in certs],ensure_ascii=False,indent=2),encoding='utf-8')
sources='# ภาพใบประกาศตัวอย่าง\n\nใช้ตามคำขอของเจ้าของพอร์ต ภาพเป็นของผู้สอน ไม่แก้ชื่อหรือข้อความบนใบ ใช้เฉพาะรายวิชาที่ตรงกับหลักสูตร\n\n'
sources+='\n'.join('- '+c['title']+': '+c['imageSource'] for c in certs if c['image'])
(ROOT/'assets/certificates/SOURCES.md').write_text(sources+'\n',encoding='utf-8')
(ROOT/'assets/tools/SOURCES.md').write_text('# Logo sources\n\nLogos identify tools used as course examples. No endorsement is implied.\n\n'+'\n'.join('- '+k+': '+v['source'] for k,v in logos.items())+'\n\nSimple Icons: https://github.com/simple-icons/simple-icons/blob/develop/LICENSE.md\n',encoding='utf-8')
export=data+'\nconsole.log(JSON.stringify({categories,tools,weeks}));'
course=json.loads(subprocess.check_output(['node'],input=export,encoding='utf-8'))
(SRC/'course.json').write_text(json.dumps(course,ensure_ascii=False,indent=2),encoding='utf-8')
print('Built standalone presentation:',output.name,len(html.encode('utf-8')),'bytes; 16 weeks, 9 subjects, 5 evidence paths, 3 certificate images')
