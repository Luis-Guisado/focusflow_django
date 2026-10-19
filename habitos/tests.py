from django.test import TestCase
from django.urls import reverse

from .forms import HabitoForm
from .models import Categoria, Habito, RegistroHabito

# Create your tests here.
class ModelosTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Salud")
        self.habito = Habito.objects.create(
            nombre="Tomar agua", categoria=self.categoria, meta_semanal=7
        )
        
    def test_str_categoria(self):
        self.assertEqual(str(self.categoria), "Salud")
        
    def test_str_habito(self):
        self.assertEqual(str(self.habito), "Tomar agua")
        
    def test_valores_por_defecto(self):
        self.assertEqual(self.habito.frecuencia, "diario")
        self.assertTrue(self.habito.activo)
        
    def test_registro_habito(self):
        registro = RegistroHabito.objects.create(habito=self.habito)
        self.assertTrue(registro.completado)
        self.assertIsNotNone(registro.fecha)
        self.assertIn("Tomar agua", str(registro))
        
    def test_eliminar_categoria_elimina_sus_habitos(self):
        self.categoria.delete()
        self.assertEqual(Habito.objects.count(), 0)
        
class FormularioTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Estudio")
        
    def datos(self, **cambios):
        datos = {
            "nombre": "Leer 30 minutos",
            "descripcion": "Lectura diaria",
            "frecuencia": "diario",
            "meta_semanal": 5,
            "categoria": self.categoria.pk,
            "activo": True,
        }
        datos.update(cambios)
        return datos
    
    def test_formulario_valido(self):
        form = HabitoForm(data=self.datos())
        self.assertTrue(form.is_valid())
        
    def test_meta_mayor_a_7_es_invalida(self):
        form = HabitoForm(data=self.datos(meta_semanal=9))
        self.assertFalse(form.is_valid())
        self.assertIn("meta_semanal", form.errors)
        
    def test_meta_cero_es_invalida(self):
        form = HabitoForm(data=self.datos(meta_semanal=0))
        self.assertFalse(form.is_valid())
        
    def test_nombre_es_obligatorio(self):
        form = HabitoForm(data=self.datos(nombre=""))
        self.assertFalse(form.is_valid())
        self.assertIn("nombre", form.errors)
        
class VistasTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Salud")
        self.habito = Habito.objects.create(
            nombre="Hacer ejercicio", categoria=self.categoria, meta_semanal=6
        )
        self.url_lista = reverse("habitos:listar_habitos")
        
    def test_listar_habitos(self):
        respuesta = self.client.get(self.url_lista)
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Hacer ejercicio")
        self.assertTemplateUsed(respuesta, "habitos/lista_habitos.html")
        
    def test_crear_habito_muestra_formulario(self):
        respuesta = self.client.get(reverse("habitos:crear_habito"))
        self.assertEqual(respuesta.status_code, 200)
        
    def test_crear_habito_guarda_y_redirige(self):
        datos = {
            "nombre": "Meditar",
            "descripcion": "",
            "frecuencia": "diario",
            "meta_semanal": 7,
            "categoria": self.categoria.pk,
            "activo": True,
        }
        respuesta = self.client.post(reverse("habitos:crear_habito"), datos)
        self.assertRedirects(respuesta, self.url_lista)
        self.assertTrue(Habito.objects.filter(nombre="Meditar").exists())
        
    def test_crear_habito_invalido_no_guarda(self):
        datos = {
            "nombre": "Inválido",
            "frecuencia": "diario",
            "meta_semanal": 9,
            "categoria": self.categoria.pk,
        }
        respuesta = self.client.post(reverse("habitos:crear_habito"), datos)
        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(Habito.objects.filter(nombre="Inválido").exists())
        
    def test_editar_habito(self):
        datos = {
            "nombre": "Ejercicio y estiramiento",
            "descripcion": "",
            "frecuencia": "diario",
            "meta_semanal": 5,
            "categoria": self.categoria.pk,
            "activo": True,
        }
        url = reverse("habitos:editar_habito", args=[self.habito.pk])
        respuesta = self.client.post(url, datos)
        self.assertRedirects(respuesta, self.url_lista)
        self.habito.refresh_from_db()
        self.assertEqual(self.habito.nombre, "Ejercicio y estiramiento")
        
    def test_editar_habito_inexistente_da_404(self):
        respuesta = self.client.get(reverse("habitos:editar_habito", args=[999]))
        self.assertEqual(respuesta.status_code, 404)
        
    def test_eliminar_pide_confirmacion(self):
        url = reverse("habitos:eliminar_habito", args=[self.habito.pk])
        respuesta = self.client.get(url)
        self.assertEqual(respuesta.status_code, 200)
        self.assertTrue(Habito.objects.filter(pk=self.habito.pk).exists())
        
        
    def test_eliminar_habito(self):
        url = reverse("habitos:eliminar_habito", args=[self.habito.pk])
        respuesta = self.client.post(url)
        self.assertRedirects(respuesta, self.url_lista)
        self.assertFalse(Habito.objects.filter(pk=self.habito.pk).exists())