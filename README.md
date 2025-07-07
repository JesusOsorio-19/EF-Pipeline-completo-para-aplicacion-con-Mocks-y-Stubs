# EF-Pipeline-completo-para-aplicacion-con.Mocks-y-Stubs

## Jesus Diego Osorio Tello - 20211372J

**Declaro que esta entrega fue realizada sin ayuda externa ni herramientas automáticas**

### Instrucciones

1. Instalar las dependencias de requirements.txt

    ```sh
    pip install -r requirements.txt
    ```

2. Dar permiso de ejecución al script `tests/stubs/fake-analyzer.sh`

    ```sh
    chmod +x tests/stub/fake-analyzer.sh
    ```

3. Ejecutar los test, podemos hacerlo directamente todos o uno por uno

    ```sh
    # Si estamos en la carpeta raíz
    pytest tests/

    # Y si estamos en la carpeta test
    pytest

    #Ejecutar test por test
    pytest tests/test_analyzer.py

    pytest tests/test_api_client.py

    pytest tests/test_auth.py
    ```
