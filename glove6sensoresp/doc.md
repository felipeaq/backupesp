##Comunicação bilateral ClassicBT (SPP)

O principal intuito deste código é efetuar a comunicação bilateral do ClassicBT via SPP[^1].
O código foi feito unindo dois códigos _Public Domain(CC0)_, exemplos disponíveis no ESP-IDF, com os nomes de: **Acceptor** e **Initiator**. Além de incrementar a lógica de comunicação necessária para a nossa aplicação. 
Este documento será dividido nos seguintes índices:
* [Definição de variáveis e constantes](#const)
* [Funções nativas e de configuração Bluetooth](#bt)
* [Lógica de comunicação](#comlog)

####Definição de variáveis e constantes {#const}

Logo no inicio do código, ja é possivel detectar as declarações das seguintes variáveis:
```c
#define SPP_TAG "SPP_ACCEPTOR_DEMO"
#define SPP_SERVER_NAME "SPP_SERVER"
#define EXAMPLE_DEVICE_NAME "ESP_SPP_ACCEPTOR"
```
A função das duas primeiras é igual. Já a terceira, é utilizada para nomear o dispositivo, quando o mesmo for procurado por outro via Bluetooth.
As duas primeiras _TAG's_, são utilizadas apenas para nomear de qual lugar está sendo emitido o log. Existem diversos tipos de funções de log, cada uma apresenta a informação de uma forma diferente. Para saber mais sobre cada uma, consultar [documentação ESP-IDF sobre log](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/log.html).
Para a exemplificar as _TAG's_, podemos utilizar a função **ESP_LOGI**, que tem o seguinte formato:
```c
ESP_LOGI(tag, format, ... )
```
Onde os parametros são:
* **tag :** Escrita padrão, para localizar a origem do log e qual seu nível.
* **format :** Mensagem que deseja emitir ao console.
* **...** : Declaração de quaisquer que sejam as variáveis utilizadas na mensagem do log, no mesmo formato da função _printf_.

Logo, quando chamada a função, da seguinte forma:
```c
ESP_LOGI(SPP_TAG, "Hello!");
```
Irá emitir um _Hello!_ no console, e demonstrar que a mesma foi emitida via **SPP_ACCEPTOR_DEMO**.
Continuando o código, podemos encontrar:
```c
static const esp_spp_mode_t esp_spp_mode = ESP_SPP_MODE_CB;

static uint32_t addr_holder; 
static uint8_t write_flag=1, cong_flag=0;
static const esp_spp_sec_t sec_mask = ESP_SPP_SEC_AUTHENTICATE;
static const esp_spp_role_t role_slave = ESP_SPP_ROLE_SLAVE;

#define SPP_DATA_LEN 2048
static uint8_t spp_data[SPP_DATA_LEN];
```
Todas são bem intuitivas, devido ao nome. No entanto, será escrito uma descrição para cada uma, caso não fique bem claro.
* **esp_spp_mode** : Define o modo no qual o SPP irá operar. Neste código, foi definido em _callback_, ou seja, em chamadas de eventos.
* **addr_holder** : Como o próprio nome já diz, variável que irá armazenar o endereço do dispositivo que enviou a mensagem para o ESP. Este endereço é armazenado, caso seja necessário enviar alguma mensagem para o mesmo, posteriormente.
* **write_flag** & **cong_flag** : Ambas foram criadas para contemplar a lógica de comunicação utilizada.
    * **write_flag** : Utilizada para sinalizar quando um evento de escrita via _esp_spp_write()_ é completo. Onde:
        * 1 : _true_.
        * 0 : _false_. 

        O intuito desta _flag_ é evitar um evento de congestionamento de pacotes (_CONG_EVENT_).
    * **cong_flag** : Utilizada para sinalizar quando um evento de congestionamento de pacotes ocorre. Onde:
        * 1 : _true_.
        * 0 : _false_.

        O Intuito desta _flag_ é chamar um _delay_ no envio de pacotes, caso seja detectado um evento de congestionamento. Desta forma o ESP consegue finalizar o envio dos pacotes.
* **sec_mask** : Define o tipo de segurança da conexão bluetooth. Para esse caso foi utilizado: _ESP_SPP_SEC_AUTHENTICATE_. Logo, será necessário autenticação para completar a conexão via Bluetooth.
* **role_slave** : Variável utilizada para definer o _role_ do dispositivo como 'mestre' ou 'escravo'. Para esta aplicação foi utilizado _ESP_SPP_ROLE_SLAVE_ (define como 'escravo').
* **SPP_DATA_LEN** : Constante que define o tamanho do buffer (em bits) enviado via _esp_spp_write()_.
* **spp_data** : Buffer de dados que serão enviados via _esp_spp_write()_.

####Funções nativas e de configuração Bluetooth {#bt}
Para a configuração do Bluetooth, precisamos inicializar algumas funções e verificar se sua ativação foi concluída. Logo, é preciso ter o conhecimento das constantes que algumas funções de ativação Bluetooth retornam.
Comumente são utilizadas as seguintes constantes:
* **ESP_OK** : Quando foi concluído com sucesso.
* **ESP_FAIL** :  Quando foi impossível concluir por algum motivo.
Além destas, também é possível, que a função retorne algumas constantes que sinalizam qual erro impossibilitou que a inicialização da mesma fosse concluída.

Para mais informações sobre as constantes de retorno, consultar a documentação do ESP, da função desejada.
Será analisada toda a função:
````c
void startClassicBtSpp(void)
{

    // Código a ser analisado.

}
````
Primeiramente, é inicializada a partição NVS[^2]. Através de:
````c
nvs_flash_init(); 
````
Se a inicialização não for completada, e o motivo for algum dos expostos na condição do _if_, é feito limpeza da memória _'Flash NVS'_. O argumento de retorno da função **nvs_flash_erase**, é colocado como argumento de entrada na função **ESP_ERROR_CHECK**. Esta função, como o próprio nome diz, verifica se ocorreu algum erro e gera um log completo.
Após isto, é feita a inicialização do _'Flash NVS'_ novamente, como pode ser visto em:
````c
if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) 
{
    ESP_ERROR_CHECK(nvs_flash_erase());
    ret = nvs_flash_init();
}
````
O argumento de saída, é salvo na variável _ret_, e inserido como entrada na função **ESP_ERROR_CHECK** novamente.
````c
ESP_ERROR_CHECK( ret );
ESP_ERROR_CHECK(esp_bt_controller_mem_release(ESP_BT_MODE_BLE));
````
A função exposta acima, **esp_bt_controller_mem_release**, serve para liberar a memória pré-alocada para a inicialização dos tipos de Bluetooth. Como neste caso utilizamos o ClassicBT (SPP), podemos liberar a memória que seria utilizada para inicializar o BLE[^3].
Após isto, é recebida as configurações _default_ do Controlador, via **BT_CONTROLLER_INIT_CONFIG_DEFAULT**. Essas configurações, são inseridas como argumento de entrada na função **esp_bt_controller_init**, e feita uma checagem para ver se tudo ocorreu conforme o esperado. O que pode ser visto nas seguintes linhas de código:
````c
// Armazenamento das configurações default
esp_bt_controller_config_t bt_cfg = BT_CONTROLLER_INIT_CONFIG_DEFAULT();

// Inicialização do Controlador
ESP_LOGI(SPP_TAG, "Call esp_bt_controller_init(&bt_cfg)");
if ((ret = esp_bt_controller_init(&bt_cfg)) != ESP_OK)
{
    ESP_LOGE(SPP_TAG, "%s initialize controller failed: %s\n", __func__, esp_err_to_name(ret));
    return;
}
````
Com a inicialização do Controlador completa, podemos partir para a habilitação do mesmo, como pode ser visto em:
````c
// Habilitação do Controlador
ESP_LOGI(SPP_TAG, "Call esp_bt_controller_enable(ESP_BT_MODE_CLASSIC_BT)");
if ((ret = esp_bt_controller_enable(ESP_BT_MODE_CLASSIC_BT)) != ESP_OK)
{
    ESP_LOGE(SPP_TAG, "%s enable controller failed: %s\n", __func__, esp_err_to_name(ret));
    return;
}
else
{
    ESP_LOGI(SPP_TAG, "Enable controller ok");
}
````
Para nossa aplicação, o controlador foi habilitado no modo Classic Bluetooth.
Após habilitar o controlador, podemos partir para a inicialização e habilitação do Bluedroid, como pode ser visto em:
````c
// Inicialização do Bluedroid
ESP_LOGI(SPP_TAG, "Call esp_bluedroid_init()");
if ((ret = esp_bluedroid_init()) != ESP_OK) 
{
    ESP_LOGE(SPP_TAG, "%s initialize bluedroid failed: %s\n", __func__, esp_err_to_name(ret));
    return;
}
else
{
    ESP_LOGI(SPP_TAG, "Initialize bluedroid ok");
}
// Habilitação do Bluedroid  
ESP_LOGI(SPP_TAG, "Call esp_bluedroid_enable()");
if ((ret = esp_bluedroid_enable()) != ESP_OK) 
{
    ESP_LOGE(SPP_TAG, "%s enable bluedroid failed: %s\n", __func__, esp_err_to_name(ret));
    return;
}
else
{
    ESP_LOGI(SPP_TAG, "Enable bluedroid ok");
}
````
Com o bluedroid pronto para utilização, podemos registrar as funções que serão chamadas no _callback_ do GAP[^4] e do SPP, além de inicializar o SPP. O que pode ser descrito pelas seguintes linhas de código:
````c
// Registro da função de callback do GAP
ESP_LOGI(SPP_TAG, "Call esp_bt_gap_register_callback(esp_bt_gap_cb)");
if ((ret = esp_bt_gap_register_callback(esp_bt_gap_cb)) != ESP_OK) {
    ESP_LOGE(SPP_TAG, "%s gap register failed: %s\n", __func__, esp_err_to_name(ret));
    return;
}
else
{
    ESP_LOGI(SPP_TAG, "Gap register ok");
}

// Registro da função de callback do SPP   
ESP_LOGI(SPP_TAG, "Call esp_spp_register_callback(esp_spp_cb)");
if ((ret = esp_spp_register_callback(esp_spp_cb)) != ESP_OK) 
{
    ESP_LOGE(SPP_TAG, "%s spp register failed: %s\n", __func__, esp_err_to_name(ret));
    return;
}
else
{
    ESP_LOGI(SPP_TAG, "spp register ok");
}

// Inicialização do SPP   
ESP_LOGI(SPP_TAG, "Call esp_spp_init(esp_spp_mode)");
if ((ret = esp_spp_init(esp_spp_mode)) != ESP_OK) 
{
    ESP_LOGE(SPP_TAG, "%s spp init failed: %s\n", __func__, esp_err_to_name(ret));
    return;
}
else
{
    ESP_LOGI(SPP_TAG, "spp init ok");
}
````
Após a conclusão, os parametros de segurança são definidos:
````c
ESP_LOGI(SPP_TAG, "Set default parameters for Secure Simple Pairing");
esp_bt_sp_param_t param_type = ESP_BT_SP_IOCAP_MODE; // Modo IO
esp_bt_io_cap_t iocap = ESP_BT_IO_CAP_IO; // Comparação de PINS
esp_bt_gap_set_security_param(param_type, &iocap, sizeof(uint8_t));

ESP_LOGI(SPP_TAG, "Set default parameters");
esp_bt_pin_type_t pin_type = ESP_BT_PIN_TYPE_VARIABLE; // Pin Variável
esp_bt_pin_code_t pin_code;
esp_bt_gap_set_pin(pin_type, 0, pin_code);
 
ESP_LOGI(SPP_TAG, "void startClassicBtSpp(void) - End");
````
Para mais informação sobre cada constante disposta acima, verificar o [header do _GAP_](https://github.com/espressif/arduino-esp32/blob/master/tools/sdk/include/bt/esp_gap_bt_api.h).
Caso haja necessidade de saber a definição de cada evento de _callback_. Consultar as seguintes documentações:
* [SPP API - ESP32 (**_Callback_ do SPP**)](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/bluetooth/esp_spp.html)
* [GAP API - ESP32 (**_Callback_ do GAP**)](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/bluetooth/esp_gap_ble.html)

####Lógica de comunicação {#comlog}
Através do conceito de _Tasks_(FreeRTOS), foi criada toda lógica de comunicação.
Após a comunicação SPP ser estabelecida, é necessário que o ESP receba o número '1' em ASCII, ou seja, '49' em decimal. Quando o ESP recebe este dado via Bluetooth, a _Task_ é criada e os dados são enviados de forma continua. Explícito no seguinte trecho de código:
````c
static void esp_spp_cb(esp_spp_cb_event_t event, esp_spp_cb_param_t *param){
    
    // (trecho de código suprimido, para uma melhorar visualização.)

    switch (event) {

    // (trecho de código suprimido, para uma melhorar visualização.)

        case ESP_SPP_DATA_IND_EVT: // Evento que ocorre quando um dado é recebido pelo ESP

        // (trecho de código suprimido, para uma melhorar visualização.)

        addr_holder=param->srv_open.handle; // Armazena endereço de quem enviou o dado recebido.
        
        if(*(param->data_ind.data)==49) 
        {
        // Task criada fixa ao núcleo 1 do ESP. ESP contém núcleos de nº: 0 e 1.
        xTaskCreatePinnedToCore(vTask1, "SPP_WRITE_TASK", 2048, NULL, 4, NULL, 1); 
        } 
    }
}
````
A _Task_ foi criada fixa ao núcleo 1, para contentar a lógica. Já que, a variação de núcleos da _Task_, poderia quebrar o código, visto que a mesma é sequencial com os processos do Bluetooth.
Para o funcionamento da _Task_, duas variáveis locais são criadas:
* **spp_sent_index** : Conta quantas vezes a função esp_spp_write foi chamada.
* **start_time_tick** & **time_in_ticks** :
    * **start_time_tick** : Armazena o tick em que a _Task_ iniciou.
    * **time_in_ticks** : Armazena a diferença entre o tick atual e o tick em que a _Task_ iniciou.

Após entrar no loop infinito, algumas condições são impostas:
1. Caso haja um evento de congestionamento, ou seja, **cong_flag** diferente de '0', um _Delay_ de 40ms é chamado. Isto ocorre para que o ESP consiga concluir o envio dos pacotes em congestionamento, sem perder os mesmos.
2. A função **esp_spp_write** só vai ser chamada caso a escrita anterior tenha sido concluída, ou seja, **write_flag** igual a '1'. 
3. Após chegar no final da _Task_, um _Delay_ de 15ms é chamado. Isto ocorre para que a _Idle Task_ entre em funcionamento e limpe o que for necessário.

Para efetuar alguns testes de _Throughput_, foi criada uma rotina de 10s. 
Um buffer de 2KBytes é enviado de forma constante, durante 10s. Após o término do tempo, a _Task_ é deletada e o **spp_sent_index** zerado. A _Task_ só será criada novamente, quando o ESP receber o digito '1' em ASCII.
O trecho explicado é referente ao seguinte código:
````c
void vTask1(void *pvParameters){
    static uint32_t spp_sent_index=0;
    static TickType_t start_time_tick, time_in_ticks; 

    ESP_LOGI(SPP_TAG, "TASK RUNNING!");
    start_time_tick=xTaskGetTickCount();     
    for ( ;; ){
        if(cong_flag==1){
            vTaskDelay(pdMS_TO_TICKS(40));
            cong_flag=0;
        }   
        if(write_flag==1){
        esp_spp_write(addr_holder, SPP_DATA_LEN, &spp_data[0]);
        spp_sent_index++;
        write_flag=0;
        }        
        time_in_ticks=xTaskGetTickCount()-start_time_tick;
        if(time_in_ticks>=pdMS_TO_TICKS(10000)){
            ESP_LOGI(SPP_TAG, "Last 'spp_sent_index' value: %d", spp_sent_index);
            spp_sent_index=0;
            ESP_LOGI(SPP_TAG, "10s Routine completed!\nTask deleted and spp_sent_index reseted!");              
            vTaskDelete(NULL);              
        }        
        vTaskDelay( pdMS_TO_TICKS ( 15 ) );
    }

}
````
Tanto a **cong_flag**, quanto a **write_flag** são alteradas no seguinte evento:
* **ESP_SPP_WRITE_EVT**
Evento que significa que uma escrita foi concluída. 

Junto com o mesmo é recebido um parametro que sinaliza se houve congestionamento ou não. Caso haja, **cong_flag** é alterado para '1'.
Como pode ser visto em:
````c
// Este código esta no interior do case ESP_SPP_WRITE_EVT
write_flag=1;
if (param->write.cong != 0){
    cong_flag=1;
}
````
Toda a explicação efetuada, é levando em conta que o leitor já tenha um conhecimento prévio de FreeRTOS. Caso não haja, consultar a seguinte documentação:
* [Mastering the FreeRTOS Real Time Kernel – a Hands On Tutorial Guide](https://www.freertos.org/wp-content/uploads/2018/07/161204_Mastering_the_FreeRTOS_Real_Time_Kernel-A_Hands-On_Tutorial_Guide.pdf)



[^1]: Serial Port Profile.
[^2]: Non-Volatile Storage.
[^3]: Bluetooth Low-Energy.
[^4]: Generic Access Profile.