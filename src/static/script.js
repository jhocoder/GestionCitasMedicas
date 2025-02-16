document.addEventListener("DOMContentLoaded", function(){
    document.querySelectorAll(".completar-btn").forEach((button)=>{
        button.addEventListener("click", function(event){
            event.preventDefault()

            const citaid = this.getAttribute("data-id")
            const citaElemento = document.getElementById(`cita-${citaid}`)

            if (citaElemento){
                citaElemento.style.style.textDecoration = 'line-through';
            }

            setTimeout(()=>{
                window.location.href = this.href;
            }, 500)
        })
    })
})