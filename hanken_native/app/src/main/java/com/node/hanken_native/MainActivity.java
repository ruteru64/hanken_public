package com.node.hanken_native;

import android.app.PendingIntent;
import android.content.Intent;
import android.nfc.NfcAdapter;
import android.os.Bundle;
import android.util.Log;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Handler;
import android.os.Looper;
import android.widget.TextView;

import org.jetbrains.annotations.NotNull;
import org.json.JSONObject;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {

    // アダプタを扱うための変数
    private NfcAdapter mNfcAdapter;
    private String TAG = "MainActivity";
    TextView txt01;
    EditText event;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // アダプタのインスタンスを取得
        mNfcAdapter = android.nfc.NfcAdapter.getDefaultAdapter(this);

        txt01 = findViewById(R.id.txt01);
        event = findViewById(R.id.event);
    }

    @Override
    protected void onResume(){
        super.onResume();

        // NFCがかざされたときの設定
        Intent intent = new Intent(this, this.getClass());
        intent.setFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP);
        // ほかのアプリを開かないようにする
        PendingIntent pendingIntent = PendingIntent.getActivity(getApplicationContext(), 0, intent, 0);
        mNfcAdapter.enableForegroundDispatch(this, pendingIntent, null, null);

    }
    @Override
    protected void onPause(){
        super.onPause();

        // Activityがバックグラウンドになったときは、受け取らない
        mNfcAdapter.disableForegroundDispatch(this);

    }
    @Override
    protected void onNewIntent(Intent intent){
        super.onNewIntent(intent);

        // NFCのUIDを取得
        byte[] uid = intent.getByteArrayExtra(NfcAdapter.EXTRA_ID);
        String out = "";
        for (int i = 0;i<uid.length;i++){
            int tempint = uid[i];
            tempint = tempint<0?tempint+256:tempint;
            String tempS = Integer.toString(tempint,16);
            tempS = tempS.length()==1?"0"+tempS:tempS;
            out += tempS;
        }
        if (event.getText().toString() == ""){
            return;
        }
        try{
            Integer.parseInt(event.getText().toString());
        }catch(Exception e){
            return;
        }
        //httpリクエスト
        try{
            //okhttpを利用するカスタム関数（下記）
            httpRequest("https://hanken.link/hostnfcget-a"+"?id="+event.getText()+"&nfc="+out);
        }catch(Exception e){
            Log.e("Hoge",e.getMessage());
        }
        // 表示
        Toast.makeText(this,out, Toast.LENGTH_SHORT).show();
    }

    void httpRequest(String url) throws IOException{

        //OkHttpClinet生成
        OkHttpClient client = new OkHttpClient();

        //request生成
        Request request = new Request.Builder()
                .url(url)
                .build();

        //非同期リクエスト
        client.newCall(request)
                .enqueue(new Callback() {

                    //エラーのとき
                    @Override
                    public void onFailure(@NotNull Call call, @NotNull IOException e) {
                        Log.e("Hoge",e.getMessage());
                    }

                    //正常のとき
                    @Override
                    public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {

                        //response取り出し
                        final String jsonStr = response.body().string();
                        Log.d("Hoge","jsonStr=" + jsonStr);

                        //JSON処理
                        try{
                            //jsonパース
                            JSONObject json = new JSONObject(jsonStr);
                            String statust = "";
                            if (json.getString("isnfc") == "1" && json.getString("isticket") == "1" && json.getString("wasentry") == "0"){
                                statust = "入場可能";
                            }else if (json.getString("isnfc") == "1" && json.getString("isticket") == "1"){
                                statust = "再入場";
                            }else if (json.getString("isnfc") == "1"){
                                statust = "チケットが登録されていません";
                            }else{
                                statust = "登録されていないNFCです";
                            }
                            final String status = statust;

                            //親スレッドUI更新
                            Handler mainHandler = new Handler(Looper.getMainLooper());
                            mainHandler.post(new Runnable() {
                                @Override
                                public void run() {
                                    txt01.setText(status);
                                }
                            });


                        }catch(Exception e){
                            Log.e("Hoge",e.getMessage());
                        }

                    }
                });
    }
}