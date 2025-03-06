<?php
/*
https://developers.ecpay.com.tw/?p=27995


不需要跳轉到綠界付款頁面

超商代碼  虛擬帳號

*/

class ecpay{

    public array $UserAgent = [
        "Mozilla/5.0 (Linux; Android 13; SM-N981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2501.3 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; rv:41.0) Gecko/20100101 Firefox/41.0",
        "Mozilla/5.0 (Linux; Android 8.1.0; ZTE A0722) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.96 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/113.0.5672.109 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 13.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) BC3 iOS/3.12.7 (build 538; iPhone 11 Pro Max; iOS 14.7.1)",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/113.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15"
    ];
    public int $MerchantID = 0;
    public int $formaMerchantID = 3420252;
    public int $testMerchantID = 3002607;

    public string $HashKey = "";
    public string $HashIV = "";

    public string $formaHashKey = "p3rN1mvxHlU0lIm7";
    public string $formaHashIV = "bRmSW9atScH6hQZ7";

    public string $testHashKey = "pwFHCqoQZGmho4w6";
    public string $testHashIV = "EkRm7iFT261dpevs";

    public  string $server_url = "";
    //正式環境BaseUrl
    public string $formalurl = 'https://ecpayment.ecpay.com.tw/1.0.0/Cashier/GenPaymentCode';
    //測試環境BaseUrl
    public string $testurl = 'https://ecpayment-stage.ecpay.com.tw/1.0.0/Cashier/GenPaymentCode';

    //Inquire order
    public string $InquireOrder = "";
    public string $formalInquireOrder = "https://ecpayment.ecpay.com.tw/1.0.0/Cashier/QueryTrade";
    public string $testInquireOrder = "https://ecpayment-stage.ecpay.com.tw/1.0.0/Cashier/QueryTrade";

    public bool $environment = false;

    public function __construct(){

        //測試環境
        if(!$this->environment){
            $this->server_url = $this->testurl;
            $this->HashKey = $this->testHashKey;
            $this->HashIV = $this->testHashIV;
            $this->MerchantID = $this->testMerchantID;
            $this->InquireOrder = $this->testInquireOrder ;
        } else {
            //正式環境
            $this->server_url= $this->formalurl;
            $this->HashKey = $this->formaHashKey;
            $this->HashIV = $this->formaHashIV;
            $this->MerchantID = $this->formaMerchantID;
            $this->InquireOrder = $this->formalInquireOrder;
        }

    }
    public function encrypt($data):string{

        $jsonEncoded = json_encode($data);
        $urlEncoded = urlencode($jsonEncoded);
        $result = openssl_encrypt($urlEncoded,'AES-128-CBC',$this->HashKey, OPENSSL_RAW_DATA, $this->HashIV);
        return base64_encode($result);
    }

    public function decrypt($data):array{
        $bin_data=base64_decode($data);
        $decrypted = openssl_decrypt($bin_data,'AES-128-CBC', $this->HashKey, OPENSSL_RAW_DATA, $this->HashIV);

        $urlDecoded = urldecode($decrypted);

        return json_decode($urlDecoded, true);
    }

    public function ErrorMSg($Code) {
        $ecpaymsg = [];
        @include(WEBROOT."model/ecpaymsg.php");
        if($ecpaymsg[$Code]){
            return $ecpaymsg[$Code];
        } else {
            return null;
        }
    }

    public function isJSON($string) : bool{
        return is_string($string) && is_array(json_decode($string, true)) ? true : false;
    }

    //超商繳款代碼
    public function SuperPaymentCode($oid,$price,$CVSCode='CVS'): array{
        $ch = "";
        try {
            if(!extension_loaded('curl')) {
                throw new Exception('php curl no Enable');
            }

            if($CVSCode == "FAMILY"){
                $ExpireDate = '4320';
            } else {
                $ExpireDate = '10080';
            }



            $postData = [
                "MerchantID"    => $this->MerchantID,
                "ChoosePayment" =>  "CVS",
                "OrderInfo"      => [
                    "MerchantTradeDate" =>  date('Y/m/d H:i:s'),
                    "MerchantTradeNo"   =>  $oid,
                    "TotalAmount"       =>  $price,
                    "ReturnURL"         =>  $GLOBALS['HTTPHOST']."/goldflow.html",
                    "TradeDesc"         =>  "購物車清單",
                    "ItemName"          =>  "商品",
                    "Remark"            =>  "",
                ],
                "CVSInfo"       => [
                    /*
                        全家最多為 4320 分鐘 3 天
                        其他 10080 分鐘 7天
                        CVS : 超商代碼(不指定超商)，此為預設值
                        OK : OK 超商代碼
                        FAMILY: 全家超商
                        HILIFE : 萊爾富超商
                        IBON : 7 – 11 ibon
                     */
                    "ExpireDate"    =>  $ExpireDate,
                    "CVSCode"       =>  $CVSCode,
                    "Desc_1"        =>  "",
                    "Desc_2"        =>  "",
                    "Desc_3"        =>  "",
                    "Desc_4"        =>  "",
                ],
                "CustomField"   =>  "",
            ];



            $PostAllData = [
                "PlatformID"    =>  "",
                "MerchantID"    => $this->MerchantID,
                "RqHeader" => [
                    "Timestamp"         => $GLOBALS['timestamp']
                ],
                "Data"                  =>  $this->encrypt($postData),
            ];

            $headers[] = 'User-Agent:'.$this->UserAgent[mt_rand(0,14)];
            $headers[] = 'Content-Type: application/json';

            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $this->server_url);
            curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
            curl_setopt($ch, CURLOPT_POST, 1);
            curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 120);
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            //curl_setopt($ch, CURLOPT_SSLVERSION, CURL_SSLVERSION_TLSv1_2);
            curl_setopt($ch, CURLOPT_TIMEOUT, 120);
            curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 60);
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
            curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($PostAllData));

            $return =  curl_exec($ch);

            if (curl_exec($ch) === false) {
                throw new Exception(curl_error($ch));
                curl_close($ch);
            }




            if($this->isJSON($return)){

                $returndata = json_decode($return, true);

                if($returndata['TransCode'] && $returndata['TransCode'] != 1 && $this->ErrorMSg($returndata['TransCode']) != null){
                    $returndata = array('RtnCode'=>0,'RtnMsg'=>$this->ErrorMSg($returndata['TransCode']));
                } else {
                    $Data = $this->decrypt($returndata['Data']);
                    if($Data['RtnCode'] != 1){
                        $returndata = array('RtnCode'=>0,'RtnMsg'=>$Data['RtnMsg'],$Data);
                    } else {
                        $returndata['Data'] = $this->decrypt($returndata['Data']);
                    }

                }
                return $returndata;
            } else {
                throw new Exception($return);
            }

        } catch (Exception $e) {
            echo json_encode(array('state'=>false,'msg'=>$e->getMessage()),JSON_UNESCAPED_UNICODE);footer();
            exit;
        }
    }

    //虛擬帳號
    public function VirtualAccount($oid,$price) {
        $ch = "";
        try {
            if(!extension_loaded('curl')) {
                throw new Exception('php curl no Enable');
            }
            /*
            if(!$this->environment) {
                $BankCode = ['007' , '822' , '118'];
                $BankCodeData = $BankCode[mt_rand(0,2)];
            } else {
                //$BankCode = ['007' , '822' , '118' , '013'];
                $BankCode = ['007' , '822' , '118'];
                $BankCodeData = $BankCode[mt_rand(0,2)];
            }*/

            $BankCode = [ '822' , '118'];
            $BankCodeData = $BankCode[mt_rand(0,1)];


            //writeover(WEBROOT."cache/goldlogistics/VirtualAccount".date('Ymd').".txt",$BankCodeData."\n","a+");


            $postData = [
                "MerchantID"    => $this->MerchantID,
                "ChoosePayment" =>  "ATM",
                "OrderInfo"      => [
                    "MerchantTradeDate" =>  date('Y/m/d H:i:s'),
                    "MerchantTradeNo"   =>  $oid,
                    "TotalAmount"       =>  $price,
                    "ReturnURL"         =>  $GLOBALS['HTTPHOST']."/goldflow.html",
                    "TradeDesc"         =>  "購物車清單",
                    "ItemName"          =>  "商品",
                    "Remark"            =>  "",
                ],
                "ATMInfo"   =>  [
                    "ExpireDate"    => 7,
                    //第一銀行007/中國信託822/板信銀行118/國泰世華013  會回傳繳款人匯款帳號資訊
                    "ATMBankCode"       =>   $BankCodeData,
                ],
                "CustomField"   =>  "",
            ];



            $PostAllData = [
                "PlatformID"    =>  "",
                "MerchantID"    => $this->MerchantID,
                "RqHeader" => [
                    "Timestamp"         => $GLOBALS['timestamp']
                ],
                "Data"                  =>  $this->encrypt($postData),
            ];

            $headers[] = 'User-Agent:'.$this->UserAgent[mt_rand(0,14)];
            $headers[] = 'Content-Type: application/json';



            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $this->server_url);
            curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
            curl_setopt($ch, CURLOPT_POST, 1);
            curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 120);
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            //curl_setopt($ch, CURLOPT_SSLVERSION, CURL_SSLVERSION_TLSv1_2);
            curl_setopt($ch, CURLOPT_TIMEOUT, 120);
            curl_setopt($ch,CURLOPT_CONNECTTIMEOUT, 60);
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
            curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($PostAllData));

            $return =  curl_exec($ch);

            if (curl_exec($ch) === false) {
                throw new Exception(curl_error($ch));
                curl_close($ch);
            }

            $info = curl_getinfo($ch);

            //writeover(WEBROOT."cache/goldlogistics/VirtualAccountPOST".date('Ymd').".txt",valueexport($info)."\r\n","a+");
            //writeover(WEBROOT."cache/goldlogistics/VirtualAccountPOST".date('Ymd').".txt",valueexport(json_decode($return, true))."\r\n","a+");
            curl_close($ch);


            if($this->isJSON($return)){

                $returndata = json_decode($return, true);

                if($returndata['TransCode'] && $returndata['TransCode'] != 1 && $this->ErrorMSg($returndata['TransCode']) != null){
                    $returndata = array('RtnCode'=>0,'RtnMsg'=>$this->ErrorMSg($returndata['TransCode']));
                } else {
                    $Data = $this->decrypt($returndata['Data']);
                    if($Data['RtnCode'] != 1){
                        $returndata = array('RtnCode'=>0,'RtnMsg'=>$Data['RtnMsg'],$Data);
                    } else {
                        $returndata['Data'] = $this->decrypt($returndata['Data']);
                    }

                }
                return $returndata;
            } else {
                throw new Exception($return);
            }

        } catch (Exception $e) {
            echo json_encode(array('state'=>false,'msg'=>$e->getMessage()),JSON_UNESCAPED_UNICODE);footer();
            exit;
        }
    }

    public function  InquireOrder($MerchantTradeNo){

        //$this->InquireOrder
        $ch = "";
        try {
                $PostAllData = [
                    "PlatformID"    =>  "",
                    "MerchantID"    => $this->MerchantID,
                    "RqHeader" => [
                        "Timestamp"         => $GLOBALS['timestamp']
                    ],
                    "Data"                  =>  $this->encrypt(["MerchantID"=>$this->MerchantID,"MerchantTradeNo"=>$MerchantTradeNo]),
                ];

                $headers[] = 'User-Agent:'.$this->UserAgent[mt_rand(0,14)];
                $headers[] = 'Content-Type: application/json';


                $ch = curl_init();
                curl_setopt($ch, CURLOPT_URL, $this->InquireOrder);
                curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
                curl_setopt($ch, CURLOPT_POST, 1);
                curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 120);
                curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
                curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
                //curl_setopt($ch, CURLOPT_SSLVERSION, CURL_SSLVERSION_TLSv1_2);
                curl_setopt($ch, CURLOPT_TIMEOUT, 120);
                curl_setopt($ch,CURLOPT_CONNECTTIMEOUT, 60);
                curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
                curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
                curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($PostAllData));

                $return =  curl_exec($ch);
                if (curl_exec($ch) === false) {
                    throw new Exception(curl_error($ch));
                    curl_close($ch);
                }


                if($this->isJSON($return)){

                    $returndata = json_decode($return, true);

                    if($returndata['TransCode'] && $returndata['TransCode'] != 1 && $this->ErrorMSg($returndata['TransCode']) != null){
                        $returndata = array('RtnCode'=>0,'RtnMsg'=>$this->ErrorMSg($returndata['TransCode']));
                    } else {
                        $Data = $this->decrypt($returndata['Data']);
                        if($Data['RtnCode'] != 1){
                            $returndata = array('RtnCode'=>0,'RtnMsg'=>$Data['RtnMsg'],$Data);
                        } else {
                            $returndata['Data'] = $this->decrypt($returndata['Data']);
                        }

                    }

                    return $returndata;
                } else {
                    throw new Exception($return);
                }

        } catch (Exception $e) {
            echo json_encode(array('state'=>false,'msg'=>$e->getMessage()),JSON_UNESCAPED_UNICODE);footer();
            exit;
        }

    }

}


?>
