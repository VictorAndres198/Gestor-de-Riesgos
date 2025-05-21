# matriz_riesgos.py
from flask import Flask, render_template, send_file, request, redirect, flash
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from taiga_api import get_auth_token, create_project

app = Flask(__name__)
app.secret_key = "mi_clave_super_secreta"  # Puedes poner cualquier cadena segura

likelihood_scale = {
    'Rare': 1,
    'Unlikely': 2,
    'Possible': 3,
    'Likely': 4,
    'Almost Certain': 5
}

impact_scale = {
    'Insignificant': 1,
    'Minor': 2,
    'Moderate': 3,
    'Major': 4,
    'Catastrophic': 5
}

risk_criteria = {
    'Categories': ['Market Volatility', 'Regulatory Changes', 'Technology Failure', 'Competition', 'Project Management'],
    'Likelihood': list(likelihood_scale.keys()),
    'Impact': list(impact_scale.keys())
}

risks = {
    'Market Volatility': {'likelihood': 'Likely', 'impact': 'Moderate'},
    'Regulatory Changes': {'likelihood': 'Possible', 'impact': 'Major'},
    'Technology Failure': {'likelihood': 'Unlikely', 'impact': 'Minor'},
    'Competition': {'likelihood': 'Likely', 'impact': 'Minor'},
    'Project Management': {'likelihood': 'Possible', 'impact': 'Moderate'}
}

def generate_matrix_image():
    risk_scores = {}
    for risk, data in risks.items():
        risk_scores[risk] = likelihood_scale[data['likelihood']] * impact_scale[data['impact']]

    risk_matrix = pd.DataFrame(
        index=risk_criteria['Likelihood'], columns=risk_criteria['Impact'])
    for i in risk_matrix.index:
        for j in risk_matrix.columns:
            risk_matrix.loc[i, j] = likelihood_scale[i] * impact_scale[j]

    plt.figure(figsize=(10, 8))
    sns.heatmap(risk_matrix.astype(int), annot=True, cmap='RdYlGn_r', fmt='d',
                linewidths=.5, cbar_kws={'label': 'Risk Score'})
    plt.title('Risk Matrix')
    plt.xlabel('Impact')
    plt.ylabel('Likelihood')

    for risk, score in risk_scores.items():
        likelihood = risks[risk]['likelihood']
        impact = risks[risk]['impact']
        plt.text(impact_scale[impact] - 0.5, likelihood_scale[likelihood] - 0.5, risk,
                 fontsize=8, ha='center', va='center', color='black')

    output_path = os.path.join('static', 'risk_matrix.png')
    plt.savefig(output_path)
    plt.close()

@app.route('/')
def index():
    generate_matrix_image()
    return render_template('index.html')

@app.route('/image')
def get_image():
    return send_file('static/risk_matrix.png', mimetype='image/png')

@app.route('/charts')
def charts():
    return render_template('charts.html')  # Renderiza desde templates/

@app.route('/login')
def login():
    return render_template('login.html')  # Renderiza desde templates/

@app.route('/register')
def register():
    return render_template('register.html')  # Renderiza desde templates/

@app.route('/tables')
def tables():
    return render_template('tables.html')  # Renderiza desde templates/

@app.route('/password')
def password():
    return render_template('password.html')  # Renderiza desde templates/

@app.route('/layoutsidenavlight')
def layoutsidenavlight():
    return render_template('layout-sidenav-light.html')  # Renderiza desde templates/

@app.route('/layoutstatic')
def layoutstatic():
    return render_template('layout-static.html')  # Renderiza desde templates/

@app.route('/error401')
def error401():
    return render_template('401.html')  # Renderiza desde templates/

@app.route('/error404')
def error404():
    return render_template('404.html')  # Renderiza desde templates/

@app.route('/error500')
def error500():
    return render_template('500.html')  # Renderiza desde templates/

@app.route('/inicio')
def inicio():
    return render_template('Inicio.html')  # Renderiza desde templates/

@app.route('/crear')
def crear():
    return render_template('create_project.html')

@app.route('/create_project', methods=['POST'])
def create_project_route():
    name = request.form.get('name')
    description = request.form.get('description')

    try:
        token = get_auth_token()
        project = create_project(token, name, description)
        flash(f"Proyecto '{project['name']}' creado con éxito", "success")
    except Exception as e:
        flash(str(e), "danger")

    return redirect('/crear')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
