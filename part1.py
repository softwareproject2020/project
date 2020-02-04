#IMPLEMENTATION of the Web-based user interface (UI). 
#Such a UI provides a list of choices, where each choice enables an analytical objective (cf. Part 2). 
#However, the interaction between the UI and the analytical objectives is always mediated by the software Part 1. 
#The list of choices can be represented as a list of hyperlinks. 
#Each hyperlink is associated with a dedicated view (i.e. a Web page) that shows the outcomes of the analytical 
#operation requested by the user. Again the dedicated view provided by the Web page does not communicate directly with the Part 2, 
#but it communicates with the Part 1. Accordingly the Part 1 is responsible for (i) forwarding the request to the 
#appropriate class/method of Part 2 and (ii) returning the result to the view.

from flask import Flask, render_template, request
from part2 import*

app = Flask(__name__)

@app.route('/')  
def index(): 
	return render_template('part3.html')	#before the @app.route, define value (value= result of the functions), then add ex. values={}, then on html insert {{value[?]}}
	
@app.route('/result1')  
def result1():
	result1=Number().record()
	return render_template('result1.html', value={'rc': result1})

@app.route('/result2')  
def result2():
	result2=Semantics().record()
	return render_template('result2.html', value={'sm': result2})

@app.route('/result3')  
def result3():
	result3=Genes().record()
	return render_template('result3.html', gn=result3.to_html())


@app.route('/result4')
def result4():
	return render_template("result4.html")

@app.route('/biotype', methods=['POST'])
def biotype_genes():
    if request.method == 'POST':
        biotype = request.form['biotype']
        result4=AssociatedGenes().record()
    return render_template('biotype.html', **locals())

		
@app.route('/result5')  
def result5():
	result5=Chromosomes().record()
	return render_template('result5.html', value={'ch': result5})

@app.route('/result6')  
def result6():
	result6=NumberOfGenes().record()
	return render_template('result6.html', ng=result6.to_html())

@app.route('/result7')  
def result7():
	result7=PlusStrand().record()
	return render_template('result7.html', ps=result7.to_html())
@app.route('/result8')  
def result8():
	result8=MinusStrand().record()
	return render_template('result8.html', ms=result8.to_html())	



#a=Number()
#b=Chromosomes()
#classes[a,b]

#for i in classes.size() :
#	@app.route('/result'+i)
#	def result(i):
#		result=classes[i].record()
#		return render_template('result'+i+'.html', value={classes[i].split(0,2) : result})

	
if __name__ == '__main__':    
	app.run(debug=True) 
