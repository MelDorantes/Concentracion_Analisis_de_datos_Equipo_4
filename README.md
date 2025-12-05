# **Análisis integral de la flota del diagnóstico a la acción**
**Integrantes**: Valeria Gisel Concha Valdovinos, Melissa Dorantes Martínez, María Alejandra Munévar Díaz, Bruno Jasso Juárez
## **Justificación de las Tecnologías Utilizadas**
* **Web/Dashboard: Streamlit**

Se seleccionó Streamlit para el desarrollo de la aplicación web debido a su simplicidad, rapidez de implementación y facilidad para integrar modelos de machine learning y visualizaciones interactivas. Streamlit permite construir dashboards robustos sin necesidad de manejar configuraciones web complejas, lo cual acelera el desarrollo y facilita la presentación de resultados al socio formador. Además, su compatibilidad con bibliotecas como Plotly y Altair permite crear interfaces dinámicas con filtros, selectores y visualizaciones altamente interactivas.
* **Modelos Predictivos: XGBoost**

Para resolver el problema logístico planteado, el equipo seleccionó XGBoost como modelo principal de predicción debido a:

- Su excelente desempeño en problemas con alta variabilidad y relaciones no lineales, como los tiempos logísticos por ruta y condiciones operativas.
- Su capacidad para manejar outliers, variables categóricas codificadas y distribuciones irregulares.
- Su robustez frente a datos incompletos o con ruido operativo, algo común en entornos reales de transporte.
- Su ventaja respecto a modelos tradicionales de series de tiempo, que requieren estacionalidades claras, patrones estables y horizontes estrictamente temporales,       condiciones     que no se cumplen en la operación logística en este caso.
    - Sus métricas de error fueron consistentemente mejores durante la validación cruzada, mostrando mayor capacidad de generalización.

* **Manipulación de Datos: Pandas**

Se utilizó Pandas para la limpieza, transformación y manejo de los datos. Su eficiencia en la manipulación de estructuras tipo DataFrame y sus herramientas de preprocesamiento lo convierten en el estándar para análisis de datos en Python.

* **Visualización: Plotly y Altair**

-Plotly permite construir visualizaciones altamente interactivas, ideales para dashboards que requieren dinamismo, zoom, filtros y análisis exploratorio.

-Altair, por su sintaxis declarativa, permitió construir gráficos limpios y consistentes para análisis descriptivos más detallados.

El uso combinado de ambas bibliotecas permite comunicar resultados de forma clara, profesional y accesible para la toma de decisiones.

## **Instrucciones para Ejecutar la Aplicación**

1. Clonar el repositorio: `git clone <URL_DEL_REPOSITORIO>` o `cd <nombre_del_repositorio>`
2. Instalar las dependencias: `pip install -r requirements.txt`
3. Ejecutar la aplicación: `python3 -m streamlit run <Nombre del archivo en py>`
4. Abrir en el navegador la URL que indica Streamlit por ejemplo: http://localhost:8501

## **Justificación del Enfoque de Predicción**

El enfoque de predicción se centra en estimar el lead time por sucursal utilizando XGBoost debido a que el comportamiento logístico observado presenta:

-Alta variabilidad entre rutas y horarios
-Relaciones no lineales entre variables operativas (unidad, ruta, carga, hora, historial reciente)
-Presencia de outliers y ruido propio de las operaciones
-Variables categóricas que influyen en el resultado de manera compleja

Modelos tradicionales basados en series de tiempo no fueron adecuados para este caso, ya que dependen de estacionalidades claras y patrones temporales estables, los cuales no están presentes en los datos operativos. Por el contrario, XGBoost permitió capturar interacciones complejas y comportamientos irregulares sin necesidad de suposiciones estrictas sobre la estructura temporal.

Aunque la calidad del modelo mejora a medida que se enriquecen las variables (por ejemplo, incorporando rezagos, viajes en vacío o indicadores mecánicos) los resultados actuales muestran que XGBoost es el método más robusto y que mejor se ajusta al comportamiento real del sistema. Esto justifica su uso como modelo final para las proyecciones.
