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
- Su ventaja respecto a modelos tradicionales de series de tiempo, que requieren estacionalidades claras, patrones estables y horizontes estrictamente temporales, condiciones que no se cumplen en la operación logística en este caso.
- Sus métricas de error fueron consistentemente mejores durante la validación cruzada, mostrando mayor capacidad de generalización.
