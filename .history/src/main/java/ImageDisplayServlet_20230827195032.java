package servlets;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;



import com.google.gson.Gson;


public class ImageDisplayServlet extends HttpServlet {

    
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String contextPath = getServletContext().getRealPath("/");
        List<String> dogImageUrls = new ArrayList<>();
        List<String> catImageUrls = new ArrayList<>();

        // Find dog and cat image URLs
        File dogsFolder = new File(contextPath + "/images/dogs");
        File catsFolder = new File(contextPath + "/images/cats");

        if (dogsFolder.exists() && dogsFolder.isDirectory()) {
            findImageUrls(dogsFolder, dogImageUrls);
        }

        if (catsFolder.exists() && catsFolder.isDirectory()) {
            findImageUrls(catsFolder, catImageUrls);
        }

        List<List<String>> imageUrls = new ArrayList<>();
        imageUrls.add(dogImageUrls);
        imageUrls.add(catImageUrls);

        response.setContentType("application/json");
        response.setCharacterEncoding("UTF-8");
        response.getWriter().write(new Gson().toJson(imageUrls));
    }

    private void findImageUrls(File folder, List<String> imageUrls) {
        File[] files = folder.listFiles();
        if (files != null) {
            for (File file : files) {
                if (file.isDirectory()) {
                    findImageUrls(file, imageUrls);
                } else if (isImageFile(file)) {
                    imageUrls.add(file.getPath().replace(getServletContext().getRealPath("/"), ""));
                }
            }
        }
    }

    private boolean isImageFile(File file) {
        String fileName = file.getName().toLowerCase();
        return fileName.endsWith(".jpg") || fileName.endsWith(".jpeg") || fileName.endsWith(".png") || fileName.endsWith(".gif");
    }
}

    

