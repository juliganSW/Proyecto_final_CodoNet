//const URL = "http://127.0.0.1:5000";
const myApp = Vue.createApp({
  data() {
    return {
      clientes: [],
      consultaCodigo: '',
      consultaResultado: '',
      altaResultado: '',
      modificarResultado: '',
      agregarCodigo: '',
      agregarNombre: '',
      agregarApellido: '',
      agregarTipo_usuario: '',
      agregarLocalidad: '', 
      modificarCodigo: '',
      modificarNuevoNombre: '',
      modificarNuevoApellido: '',
      modificarNuevoTelefono: '',
      modificarNuevoEmail: '' 
    };
  },
  methods: {
    consultarCliente() {
      fetch(`${URL}/clientes/${this.consultaCodigo}`)
        .then(response => response.json())
        .then(cliente => {
          if (cliente) {
            this.consultaResultado = `Código: ${cliente.codigo}, Nombre: ${cliente.nombre}, Apellido: ${cliente.apellido}, Telefono: ${cliente.telefono}, Email: ${cliente.email}`;

        } else {
            this.consultaResultado = 'Cliente no encontrado';
          }
        })
        .catch(error => {
          console.error(error);
          this.consultaResultado = 'Error al realizar la consulta';
        });
    },
    agregarCliente(event) {
      event.preventDefault(); // Evitar el envío del formulario por defecto

     // Validación aquí 
      if (!this.validacionExitosa()) {
      return; // Evitar realizar la solicitud si la validación no es correcta
      }
    
      // Continuamos con el envío de los datos
      fetch(`${URL}/clientes`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          codigo: this.agregarCodigo,
          nombre: this.agregarNombre,
          apellido: this.agregarApellido,
          telefono: this.agregarTelefono,
          email: this.agregarEmail
        })
      })
        .then(response => {
          if (response.ok) {
            this.agregarCodigo = '';
            this.agregarNombre = '';
            this.agregarApellido = '';
            this.agregarTelefono = '';
            this.agregarEmail = '';
            this.listarClientes();
            alert("Alta de cliente exitosa");
          } else {
            this.altaResultado = 'Alta no efectuada';
          }
        })
        .catch(error => {
          console.error(error);
        });
    },
    validacionExitosa() {
      //Validar que todos los campos estén completos
      if (!this.agregarCodigo || !this.agregarNombre || !this.agregarApellido || !this.agregarTelefono || !this.agregarEmail) {
        alert('Por favor, complete todos los campos');
        return false;
      }
    
      //Validar que el nombre y el apellido solo contengan caracteres alfabéticos y espacios
      const nombreRegExp = /^[a-zA-Z\s]+$/;
      if (!nombreRegExp.test(this.agregarNombre) || !nombreRegExp.test(this.agregarApellido)) {
        alert("El nombre y el apellido sólo pueden contener carácteres numéricos")
        return false;
      }
    
      //Validar el formato del correo electrónico utilizando una expresión regular
      const emailRegExp = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegExp.test(this.agregarEmail)) {
        alert("Por favor ingrese un formato de mail válido")
        return false;
      }
    
      return true; // La validación es exitosa
    },

    modificarCliente() {
      fetch(`${URL}/clientes/${this.modificarCodigo}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          nombre: this.modificarNuevoNombre,
          apellido: this.modificarNuevoApellido,
          telefono: this.modificarNuevoTelefono,
          email: this.modificarNuevoEmail
        })
      })
        .then(response => {
          if (response.ok) {
            this.modificarCodigo = '';
            this.modificarNuevoNombre = '';
            this.modificarNuevoApellido = '';
            this.modificarNuevoTelefono = '';
            this.modificarNuevoEmail = '';
            this.listarClientes();
            this.modificarResultado = 'Modificación realizada';
            alert("Modificación realizada");
          } else if (response.status === 400) {
            throw new Error('Error de solicitud: Datos inválidos');
          } else if (response.status === 404) {
            throw new Error('Error de solicitud: Cliente no encontrado');
          } else {
            throw new Error('Error de solicitud: Error desconocido');
          }
        })
        .catch(error => {
          console.error(error);
          this.modificarResultado = 'Modificación no efectuada: ' + error.message;
        });
    },
    
    listarClientes() {
      fetch(URL + '/clientes')
        .then(response => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error('Error al obtener los clientes.');
          }
        })
        .then(data => {
          this.clientes = data;
        })
        .catch(error => {
          console.error(error);
          alert('Error al obtener los clientes.');
        });
    },
    eliminarCliente(codigo) {
      //Eliminamos el producto de la fila seleccionada
      fetch(URL + `/clientes/${codigo}`, { method: 'DELETE' })
          .then(response => {
              if (response.ok) {
                  // Eliminar el producto de la lista después de eliminarlo en el servidor
                  this.clientes = this.clientes.filter(cliente => cliente.codigo !== codigo);
                  alert('Cliente eliminado con exito.');
              } else {
                  // Si hubo un error, lanzar explícitamente una excepción
                  // para ser "catcheada" más adelante
                  throw new Error('Error al eliminar el cliente.');
              }
          })
          .catch(error => {
              // Código para manejar errores
              alert('Error al eliminar el cliente.');
          });
  }
  },
  mounted() {
    this.listarClientes();
  }
});
myApp.mount('#my-app');
