const URL = "http://127.0.0.1:5000";
const app = Vue.createApp({
  data() {
    return {
      productos: [],
      consultaCodigo: '',
      consultaResultado: '',
      altaResultado: '',
      modificarResultado: '',
      agregarCodigo: '',
      agregarServicio: '',
      agregarPlan: '',
      agregarPrecio: '',
      modificarCodigo: '',
      modificarNuevoServicio: '',
      modificarNuevoPlan: '',
      modificarNuevoPrecio: ''
    };
  },
  methods: {
    consultarProducto() {
      fetch(`${URL}/productos/${this.consultaCodigo}`)
        .then(response => response.json())
        .then(producto => {
          if (producto) {
            this.consultaResultado = `Código: ${producto.codigo}, Servicio: ${producto.servicio}, Plan: ${producto.plan}, Precio: ${producto.precio}`;
          } else {
            this.consultaResultado = 'Producto no encontrado';
          }
        })
        .catch(error => {
          console.error(error);
          this.consultaResultado = 'Error al realizar la consulta';
        });
    },
    agregarProducto() {
      fetch(`${URL}/productos`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          codigo: this.agregarCodigo,
          servicio: this.agregarServicio,
          plan: this.agregarPlan,
          precio: this.agregarPrecio
        })
      })
        .then(response => {
          if (response.ok) {
            this.agregarCodigo = '';
            this.agregarServicio = '';
            this.agregarPlan = '';
            this.agregarPrecio = '';
            this.listarProductos(); // Llama a la función listarProductos() para actualizar la lista después de agregar un producto
            alert("Alta de producto exitosa")
          } else {
            this.altaResultado = 'Alta no efectuada';
          }
        })
        .catch(error => {
          console.error(error);
        });
    
    
    },
    modificarProducto() {
      fetch(`${URL}/productos/${this.modificarCodigo}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          servicio: this.modificarNuevoServicio,
          plan: this.modificarNuevoPlan,
          precio: this.modificarNuevoPrecio
        })
      })
        .then(response => {
          if (response.ok) {
            this.modificarCodigo = '';
            this.modificarNuevoServicio = '';
            this.modificarNuevoPlan = '';
            this.modificarNuevoPrecio = '';
            this.listarProductos();
            this.modificarResultado = 'Modificación realizada';
            alert("Modificacion realizada")
          } else {
            this.modificarResultado = 'Modificación no efectuada';
          }
        })
        .catch(error => {
          console.error(error);
        });
    },
    listarProductos() {
      fetch(URL + '/productos')
        .then(response => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error('Error al obtener los productos.');
          }
        })
        .then(data => {
          this.productos = data;
        })
        .catch(error => {
          console.error(error);
          alert('Error al obtener los productos.');
        });
    },
    eliminarProducto(codigo) {
      
      // Eliminamos el producto de la fila seleccionada
      fetch(URL + `/productos/${codigo}`, { method: 'DELETE' })
          .then(response => {
              if (response.ok) {
                  // Eliminar el producto de la lista después de eliminarlo en el servidor
                  this.productos = this.productos.filter(producto => producto.codigo !== codigo);
                  alert('Producto eliminado con exito.');
              } else {
                  // Si hubo un error, lanzar explícitamente una excepción
                  // para ser "catcheada" más adelante
                  throw new Error('Error al eliminar el producto.');
              }
          })
          .catch(error => {
              // Código para manejar errores
              alert('Error al eliminar el producto.');
          });
  }
  },
  mounted() {
    this.listarProductos();
  }
});
app.mount('#app');
