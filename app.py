# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os # Para acceder a las variables de entorno

app = Flask(__name__)
# Configura CORS para permitir solicitudes desde tu frontend.
# En producción, reemplaza "*" con el dominio de tu frontend (ej: "https://tudominio.com")
CORS(app)

# --- Configuración de Credenciales de Correo (usando variables de entorno) ---
# ¡ADVERTENCIA! Nunca pongas tus credenciales directamente en el código.
# Estas variables deben ser definidas en tu entorno de despliegue.
# Para desarrollo local, puedes definirlas temporalmente en tu terminal o en un archivo .env.
# Necesitarás generar una "contraseña de aplicación" (App Password) en tu cuenta de Google
# si tienes la verificación en dos pasos activada, ya que tu contraseña normal no funcionará.
GMAIL_USER = os.getenv('GMAIL_USER') # Tu dirección de Gmail (ej: "juanmartinbigongiari@gmail.com")
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD') # La "contraseña de aplicación" generada para Gmail
YOUR_EMAIL_TO_RECEIVE = os.getenv('YOUR_EMAIL_TO_RECEIVE', 'juanmartinbigongiari@gmail.com') # Tu Gmail donde recibirás los mensajes

if not GMAIL_USER or not GMAIL_PASSWORD:
    print("ADVERTENCIA: Las variables de entorno GMAIL_USER y GMAIL_PASSWORD no están configuradas.")
    print("El envío de correos no funcionará sin ellas.")

@app.route('/send-email', methods=['POST'])
def send_email():
    """
    Ruta para recibir las solicitudes POST del formulario de contacto
    y enviar un correo electrónico.
    """
    try:
        data = request.json # Obtiene los datos JSON enviados desde el frontend
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

        # Validación básica de los campos
        if not name or not email or not message:
            return jsonify({'success': False, 'message': 'Faltan campos obligatorios (nombre, correo o mensaje).'}), 400

        # Crea el mensaje de correo
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{name} <{email}>" # Remitente visible en el correo
        msg['To'] = YOUR_EMAIL_TO_RECEIVE # A quién va dirigido el correo (tu Gmail)
        msg['Subject'] = f"Mensaje de Portafolio: {subject if subject else 'Sin Asunto'}"

        # Cuerpo del correo en formato HTML
        html_body = f"""
        <html>
            <head></head>
            <body>
                <p><strong>De:</strong> {name}</p>
                <p><strong>Correo del remitente:</strong> {email}</p>
                <p><strong>Asunto:</strong> {subject if subject else 'Sin Asunto'}</p>
                <br>
                <p><strong>Mensaje:</strong></p>
                <p>{message}</p>
                <br>
                <p>---</p>
                <p>Este correo fue enviado desde tu formulario de contacto del portafolio.</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(html_body, 'html'))

        # Intenta enviar el correo usando SMTP de Gmail
        with smtplib.SMTP_SSL('juanmartinbigongiari.gmail.com', 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASSWORD)
            smtp.send_message(msg)

        # Si el envío es exitoso
        return jsonify({'success': True, 'message': '¡Mensaje enviado con éxito! Te contactaré pronto.'}), 200

    except smtplib.SMTPAuthenticationError:
        print(f"Error de autenticación SMTP. Revisa GMAIL_USER y GMAIL_PASSWORD: {GMAIL_USER}")
        return jsonify({'success': False, 'message': 'Error de autenticación con el servidor de correo. Revisa tus credenciales.'}), 500
    except smtplib.SMTPConnectError as e:
        print(f"Error de conexión SMTP: {e}")
        return jsonify({'success': False, 'message': 'No se pudo conectar al servidor de correo. Posible problema de red o configuración.'}), 500
    except Exception as e:
        # Captura cualquier otro error inesperado
        print(f"Error al enviar correo: {e}")
        return jsonify({'success': False, 'message': 'Hubo un error interno al enviar tu mensaje. Inténtalo de nuevo más tarde.'}), 500

if __name__ == '__main__':
    # Ejecuta la aplicación Flask
    # En desarrollo, debug=True proporciona recarga automática y mensajes de error detallados.
    # ¡IMPORTANTE! Desactiva debug=True en producción.
    app.run(debug=True, port=5000) # El backend se ejecutará en http://localhost:5000
