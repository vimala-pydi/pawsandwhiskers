    
package servlets;

import java.io.IOException;
import java.io.PrintWriter;

import javax.json.bind.Jsonb;
import javax.json.bind.JsonbBuilder;
import javax.servlet.ServletContext;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;


public class CatsServlet extends HttpServlet {

    String[] images;
   
    public void init(){
      
      ServletContext ctx = getServletContext();
      // Get real path to images folder
      String imagePath = ctx.getRealPath("WEB-INF/images");

      images = new String[]{
        imagePath + "/cat1.jpg",
        imagePath + "/cat2.jpg",
        imagePath + "/cat3.jpg",
        imagePath + "/cat4.jpg",
        imagePath + "/cat5.jpg",
        imagePath + "/cat6.jpg"
       };


    }



	protected void doGet(HttpServletRequest request,
			HttpServletResponse response) throws ServletException, IOException {
    
                PrintWriter out = response.getWriter();

               // Set content type
               response.setContentType("application/json");

               // Construct JSON array manually
               out.print("[");

             for(int i=0; i<images.length; i++) {

              out.print("\"" + images[i] + "\"");
              if(i != images.length - 1) {
                 out.print(","); 
               }
             }
             out.print("]");
             
             out.close();              
	}

}

