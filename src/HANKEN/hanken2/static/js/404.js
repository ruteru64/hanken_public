window.onload = function() {
    var canvas = document.getElementById("my_canvas");
    var ctx = canvas.getContext("2d");

    canvas.width = document.documentElement.clientWidth - 10;
    canvas.height = document.documentElement.clientHeight - 10;

    function fitCanvasSize(hight) {
      // Canvas のサイズをクライアントサイズに合わせる
      // canvas.width = document.documentElement.clientWidth - 10;
      // canvas.height = document.documentElement.clientHeight - 10;

      // Canvas 全体を塗りつぶし
    //   ctx.fillStyle = "rgb(191, 255, 191)";
    //   ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Canvas サイズに合わせて矩形を描画
        var w = canvas.width / 2;
        var h = canvas.height ;
        
        if(hight <= h){
          return 114;
        }
        //ctx.fillStyle = "cyan";
        // ctx.fillRect(10, 10, w, h);
        ctx.strokeStyle = 'rgb(00,00,255)'; //枠線の色は青
        ctx.fillStyle = '#005bab'; //塗りつぶしの色は赤

        //左から150上から75の位置に、半径60の半円を反時計回り（左回り）で描く
        ctx.arc(w,hight, w/4*3,Math.PI*1,Math.PI*2,false);
        ctx.fill();
    }
    var count = canvas.height*1.5;
    function loop(timestamp) {
      console.log(count);
      if(fitCanvasSize(count)==114){
        return 0;
      }
      
      //window.onresize = fitCanvasSize;
      count--;
      window.requestAnimationFrame((ts) => loop(ts));
    }
    window.requestAnimationFrame((ts) => loop(ts));
  }
  //fitCanvasSize();
  //window.onresize = fitCanvasSize;