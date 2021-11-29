import cv2
import numpy as np
import cv2
import math

#funcao auxiliar para calcular a distancia de dois pontos
def distance_between(p1,p2):

    distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )

    return distance
        

def detetor_formas():
    #Leitura da imagem com formas geometricas
    img = cv2.imread('formas2.png')
    imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Caso a imagem tenha pixels com cor abaixo de 200 entao o valor dos pixels passa para 0,se
    #a cor for maior que 200, esses pixels passam para o valor máximo,que em geral é 255
    _, thrash = cv2.threshold(imgGrey,200,255, cv2.THRESH_BINARY)

    #Lista dos diferentes contornos encontrados na imagem
    contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    #vai se percorrer o contorno de cada poligno individualmente

    for contour in contours:
        #O epsilon representa a distância máxima entre a aproximação de um 
        #contorno de forma do polígono de entrada e do polígono de entrada original
        epsilon =  0.01* cv2.arcLength(contour, True)
        
        approx = cv2.approxPolyDP(contour,epsilon, True)
        
        #desenha-se os contornos de cada poligno na imagem
        cv2.drawContours(img, [approx], 0, (0, 0, 0), 2)
        
        #coordenadas para colocar o texto do nome da detecao obtida
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5
        
        #Caso do triangulo
        if len(approx) == 3:
            
            cv2.putText(img, "Triangulo", (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0))
            
        #Caso dos quadrilateros   
        elif len(approx) == 4:
            x1 ,y1, w, h = cv2.boundingRect(approx)
            #calcular a relacao entre os lados maiores e os mais pequenos
            aspectRatio = float(w)/h
            
            if aspectRatio >= 0.95 and aspectRatio <= 1.05:
                cv2.putText(img, "Quadrado", (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0))
            else:
                cv2.putText(img, "Retangulo", (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0))
        #Caso do pentagono
        elif len(approx) == 5:
            cv2.putText(img, "Pentagono", (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0))
        #Caso do Hexagono
        elif len(approx) == 6:
            cv2.putText(img, "Hexagono", (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0))
        #Caso da Estrela
        elif len(approx) == 10:
            cv2.putText(img, "Estrela", (x-30, y+4), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0))
        else:
            #Calcular os pontos mais à esquerda e mais à direita 
            leftmost = tuple(approx[approx[:,:,0].argmin()][0])
            rightmost = tuple(approx[approx[:,:,0].argmax()][0])
            topmost = tuple(approx[approx[:,:,1].argmin()][0])
            bottommost = tuple(approx[approx[:,:,1].argmax()][0])

            #print(distance_between(leftmost,rightmost))
            #print(distance_between(topmost,bottommost))
            #Condicoes para o caso em que é uma elipse e para quando é um circulo
            if abs(distance_between(leftmost,rightmost) - distance_between(topmost,bottommost)) < 15:
                cv2.putText(img, "Circulo", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0))
            elif abs(distance_between(leftmost,rightmost) - distance_between(topmost,bottommost)) > 15:
                cv2.putText(img, "Elipse", (x-55, y-20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0))
            else:
                cv2.putText(img, "Figura Desconhecida", (x, y-50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0))


    cv2.imshow("Formas Geometricas", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

detetor_formas()
