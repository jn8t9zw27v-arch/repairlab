"""Build the DOCX and PDF from one report source; uses python-docx, Pillow and reportlab."""
from pathlib import Path
import json,re,subprocess,textwrap
from PIL import Image,ImageDraw,ImageFont
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Image as RLImage,Table,TableStyle,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from xml.sax.saxutils import escape

ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs'
REPORT_NAME='Assignment_2_Project_Report_Week4'
data=json.loads((DOCS/'report-source.json').read_text(encoding='utf-8'))
replays=json.loads((ROOT/'evidence/scenario-replays.json').read_text(encoding='utf-8'))['cases']
FONTS=Path('C:/Windows/Fonts')
def font(n=28,bold=False):return ImageFont.truetype(str(FONTS/('arialbd.ttf' if bold else 'arial.ttf')),n)
def wrap(draw,text,max_width,f):
 lines=[]
 for piece in str(text).split('\n'):
  words=piece.split();line=''
  for w in words:
   candidate=(line+' '+w).strip()
   if draw.textlength(candidate,font=f)>max_width and line:lines.append(line);line=w
   else:line=candidate
  lines.append(line)
 return '\n'.join(lines)
def rect(draw,xy,text,fill='#edf3f6',outline='#57717f',size=25):
 draw.rounded_rectangle(xy,radius=13,fill=fill,outline=outline,width=3)
 x,y,x2,y2=xy;draw.multiline_text(((x+x2)/2,(y+y2)/2),wrap(draw,text,x2-x-28,font(size)),font=font(size),fill='#193a4b',anchor='mm',align='center',spacing=8)
def arrow(draw,p,q):
 draw.line([p,q],fill='#57717f',width=4)
 import math
 angle=math.atan2(q[1]-p[1],q[0]-p[0]);a=18
 draw.polygon([q,(q[0]-a*math.cos(angle-.45),q[1]-a*math.sin(angle-.45)),(q[0]-a*math.cos(angle+.45),q[1]-a*math.sin(angle+.45))],fill='#57717f')

im=Image.new('RGB',(1700,900),'white');dr=ImageDraw.Draw(im)
dr.text((45,25),'RepairLab system and control flow',font=font(35,True),fill='#172f40')
nodes=[((45,120,400,245),'User and browser UI'),((525,120,920,245),'Lexical interpreter'),((1050,120,1655,245),'Fictional appointment collection'),((525,365,920,490),'Repair policy and session state'),((1050,365,1655,490),'Action controller and active-ID check'),((45,365,400,490),'Clarify / reject / correct'),((1050,610,1655,735),'Local status change and undo'),((525,610,920,735),'Event log and visible result')]
for xy,t in nodes:rect(dr,xy,t)
for a,b in [((400,182),(525,182)),((920,182),(1050,182)),((722,245),(722,365)),((525,427),(400,427)),((400,380),(525,220)),((920,427),(1050,427)),((1350,490),(1350,610)),((1050,670),(920,670)),((525,670),(220,490))]:arrow(dr,a,b)
dr.text((1050,325),'Explicit user confirmation',font=font(23,True),fill='#086b62')
dr.text((45,790),'Solid boxes: implemented     Records and ambiguous interpretations: simulated',font=font(24),fill='#445b68')
dr.text((45,835),'Not implemented: LLM, speech, live provider, persistent personal memory',font=font(24),fill='#445b68')
im.save(DOCS/'system-diagram.png')

short=[
 [('Request','Cancel my appointment','Three candidates; no change'),('Select','Dental check / A101','Preview; all records active'),('Confirm','Confirm cancellation','A101 cancelled locally'),('Recover','Undo last cancellation','A101 active again')],
 [('Request','Cancel my appointment','Two candidates; Friday omitted'),('Reject','None of these','Free-text correction invited'),('Clarify','Friday','A103 preview; no change'),('Confirm','Confirm cancellation','Only A103 cancelled')],
 [('Request','Cancel dental','A101 preview; no change'),('Correct','Go back and correct','A101 proposal discarded'),('Replace','eye','A102 preview; no change'),('Confirm','Confirm cancellation','A102 cancelled; A101 active')]
]
for i,frames in enumerate(short):
 im=Image.new('RGB',(1800,420),'white');dr=ImageDraw.Draw(im)
 for j,(phase,user,system) in enumerate(frames):
  x=15+j*450
  dr.rounded_rectangle((x,15,x+425,400),radius=13,fill='#f4f7f9',outline='#b1c2cd',width=2)
  dr.text((x+20,35),f'{j+1}  {phase}',font=font(29,True),fill='#193a4b')
  dr.text((x+20,100),'USER',font=font(18,True),fill='#58737d')
  dr.multiline_text((x+20,132),wrap(dr,user,380,font(27)),font=font(27),fill='#172f40',spacing=7)
  dr.text((x+20,235),'SYSTEM',font=font(18,True),fill='#58737d')
  dr.multiline_text((x+20,268),wrap(dr,system,380,font(25)),font=font(25),fill='#245e59',spacing=7)
 im.save(DOCS/f'storyboard-{i+1}.png')

status=[['Component','Status'],['Interface and action controller','Implemented'],['Records and omitted interpretation','Simulated'],['LLM and live provider','Not implemented']]
main_words=sum(len(p.split()) for s in data['sections'] for p in s['paragraphs'])+sum(len(s['heading'].split()) for s in data['sections'])+sum(len(c.split()) for row in status for c in row)
abstract_words=len(data['abstract'].split())
assert main_words<=1100 and abstract_words<=300 and main_words+abstract_words<=1300
readme=(ROOT/'README.md').read_text(encoding='utf-8')
without_code=re.sub(r'```.*?```','',readme,flags=re.S)
prose_count=len(re.sub(r'[#*`\[\]()]','',without_code).split())
readme=re.sub(r'README prose word count:.*',f'README prose word count: approximately {prose_count} (excluding code blocks and setup commands).',readme)
(ROOT/'README.md').write_text(readme,encoding='utf-8')
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
meta=f'Main report {main_words} words | Abstract {abstract_words} words | Total {main_words+abstract_words} words'
source_note=f'Public repository: not yet published. Local source checkpoint: {commit[:12]}. README: ../README.md.'

doc=Document()
for st in doc.styles:
 for border in list(st.element.iter(qn('w:pBdr'))):border.getparent().remove(border)
sec=doc.sections[0];sec.page_width=Inches(8.5);sec.page_height=Inches(11);sec.top_margin=sec.bottom_margin=Inches(.65);sec.left_margin=sec.right_margin=Inches(.78)
for style in ['Normal','Title','Heading 1','Heading 2','Caption']:
 doc.styles[style].font.name='Calibri';doc.styles[style].font.color.rgb=RGBColor(0,0,0)
doc.styles['Normal'].font.size=Pt(11);doc.styles['Normal'].paragraph_format.line_spacing=1.08;doc.styles['Normal'].paragraph_format.space_after=Pt(8)
doc.styles['Title'].font.size=Pt(21);doc.styles['Title'].paragraph_format.space_after=Pt(8)
doc.styles['Heading 1'].font.size=Pt(14);doc.styles['Heading 1'].paragraph_format.space_after=Pt(9)
doc.styles['Caption'].font.size=Pt(9);doc.styles['Caption'].font.italic=True
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='BodyReport',fontName='Helvetica',fontSize=10.7,leading=14,spaceAfter=8));styles.add(ParagraphStyle(name='SmallReport',fontName='Helvetica',fontSize=8.5,leading=11,spaceAfter=7));styles.add(ParagraphStyle(name='TitleReport',fontName='Helvetica-Bold',fontSize=21,leading=25,spaceAfter=10));styles.add(ParagraphStyle(name='HeadReport',fontName='Helvetica-Bold',fontSize=14,leading=18,spaceBefore=8,spaceAfter=9));styles.add(ParagraphStyle(name='CaptionReport',fontName='Helvetica-Oblique',fontSize=8.5,leading=11,spaceAfter=9))
flow=[];W=6.94*72
def text(t,style='body'):
 ds={'body':'Normal','title':'Title','head':'Heading 1','small':'Normal','caption':'Caption'}[style]
 p=doc.add_paragraph(t,style=ds)
 if style=='small':
  for r in p.runs:r.font.size=Pt(9)
 rs={'body':'BodyReport','title':'TitleReport','head':'HeadReport','small':'SmallReport','caption':'CaptionReport'}[style]
 flow.append(Paragraph(escape(t),styles[rs]))
def page():doc.add_page_break();flow.append(PageBreak())
def picture(file,width,caption):
 p=doc.add_paragraph();p.paragraph_format.keep_with_next=True;p.add_run().add_picture(str(DOCS/file),width=Inches(width))
 im=Image.open(DOCS/file);flow.append(RLImage(str(DOCS/file),width=width*72,height=width*72*im.height/im.width));text(caption,'caption')
def section(index):
 s=data['sections'][index];text(s['heading'],'head')
 for p in s['paragraphs']:text(p)
text(data['title'],'title');text('Assignment 2 Project Report','small');text(meta,'small');text('Abstract','head');text(data['abstract']);section(0)
page();section(1)
page();section(2);picture('system-diagram.png',6.9,'Figure 1. Implemented control flow with simulated data and explicit unimplemented components.')
t=doc.add_table(rows=0,cols=2);t.alignment=WD_TABLE_ALIGNMENT.CENTER
for i,row in enumerate(status):
 cells=t.add_row().cells
 for j,cell in enumerate(cells):
  cell.text=row[j];cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
  pr=cell._tc.get_or_add_tcPr();b=OxmlElement('w:tcBorders')
  for e in ['top','left','bottom','right']:
   edge=OxmlElement('w:'+e);edge.set(qn('w:val'),'single');edge.set(qn('w:sz'),'4');edge.set(qn('w:color'),'D9D9D9');b.append(edge)
  pr.append(b)
  if i==0:
   sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'E7EDF2');pr.append(sh)
  for p in cell.paragraphs:
   for r in p.runs:r.font.size=Pt(9);r.bold=i==0
 trpr=t.rows[i]._tr.get_or_add_trPr();trpr.append(OxmlElement('w:cantSplit'))
 if i==0:trpr.append(OxmlElement('w:tblHeader'))
rt=Table(status,colWidths=[W*.67,W*.33]);rt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e7edf2')),('GRID',(0,0),(-1,-1),.5,colors.HexColor('#d9d9d9')),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7)]));flow.append(rt)
page();text('Storyboards','head')
for i,caption in enumerate(['Correct candidate selection followed by confirmation and undo.','Rejection and repair when the intended record is omitted.','Correction replaces a pending interpretation before any cancellation.']):picture(f'storyboard-{i+1}.png',6.9,f'Figure {i+2}. {caption}')
page();section(3);picture('ui-options.png',4.55,'Figure 5. Actual browser view of candidate clarification and its rejection control.')
page();text('Repository and development evidence','head');text(source_note,'small');text('Development record and AI assistance are in README.md; executable checks and replay traces are in evidence/.','small');text('References','head')
for r in data['references']:
 text(r['text'],'small')
 if r['url']:text(r['url'],'small')
doc.core_properties.title=data['title'];doc.core_properties.author='';doc.save(DOCS/(REPORT_NAME+'.docx'))
def footer(canvas,document):
 canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#5b6975'));canvas.drawRightString(7.72*72,.35*72,str(document.page))
pdf=SimpleDocTemplate(str(DOCS/(REPORT_NAME+'.pdf')),pagesize=(612,792),leftMargin=.78*72,rightMargin=.78*72,topMargin=.65*72,bottomMargin=.65*72,title=data['title'],author='')
pdf.build(flow,onFirstPage=footer,onLaterPages=footer)
(ROOT/'evidence/word-counts.json').write_text(json.dumps({'abstract':abstract_words,'main_including_headings_and_status_table':main_words,'total':main_words+abstract_words,'method':'whitespace split; excludes title, references, repository links, captions and short figure labels','source_checkpoint':commit},indent=2),encoding='utf-8')
print(meta);print('Wrote DOCX, PDF, architecture and three storyboards.')
