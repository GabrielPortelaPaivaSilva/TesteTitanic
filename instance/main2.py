from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

data = {
    'PassengerId': [1, 2, 3, 4, 5],
    'Pclass': [3, 1, 3, 1, 3],
    'Name': ['João', 'Maria', 'Carlos', 'Helena', 'Marcos'],
    'Sex': ['masculino', 'feminino', 'masculino', 'feminino', 'masculino'],
    'Age': [22, 28, 35, 40, None],
    'SibSp': [0, 1, 1, 0, 0],
    'Parch': [0, 0, 0, 0, 0],
    'Fare': [7.25, 71.28, 8.05, 53.1, 8.05],
    'Embarked': ['Porto1', 'Porto2', 'Porto1', 'Porto2', 'Porto1'],
    'Survived': [0, 1, 1, 1, 0]
}
df = pd.DataFrame(data)


# Endpoint 1:
@app.route('/api/summary', methods=['GET'])
def summary():
    return jsonify(df.describe().to_dict())


# Endpoint 2:
@app.route('/api/survival_rate', methods=['GET'])
def survival_rate():
    survival_rate = df['Survived'].mean() * 100
    return jsonify({'survival_rate': survival_rate})


# Endpoint 3:
@app.route('/api/grouped/<column>', methods=['GET'])
def grouped_survival_rate(column):
    column = column.capitalize()
    if column not in df.columns:
        return jsonify({'error': f'Coluna {column} não encontrada'}), 400
    grouped = df.groupby(column)['Survived'].mean().reset_index()
    return jsonify(grouped.to_dict(orient='records'))


# Endpoint 4:
@app.route('/api/clean_data', methods=['POST'])
def clean_data():
    data = request.get_json()
    df_clean = pd.DataFrame(data)

    # Preencher valores ausentes de Age com a média
    df_clean['Age'].fillna(df_clean['Age'].mean(), inplace=True)
    # Preencher valores ausentes de Embarked com o modo (mais frequente)
    df_clean['Embarked'].fillna(df_clean['Embarked'].mode()[0], inplace=True)

    # Remover valores de Fare muito altos
    df_clean = df_clean[df_clean['Fare'] < 500]

    return jsonify(df_clean.to_dict(orient='records'))


# Endpoint 5:
@app.route('/api/correlation', methods=['GET'])
def correlation():
    return jsonify(df.corr().to_dict())


if __name__ == '__main__':
    app.run(debug=True)
