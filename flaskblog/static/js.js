   function reset_animation(slide,n){
         var elm = slide;
         var count=n
         var newone = elm.cloneNode(true);
         elm.parentNode.replaceChild(newone, elm);

         var bars = document.getElementsByClassName("bar");
         for(var i=0;i<bars.length;i++){
             //bars[i].className +=" active"
             bars[i].className = bars[i].className.replace(" active", "");
         }
         bars[n-1].className += " active";
     }