import cv2
import numpy as np
import math

#Funcao auxiliar para calcular a distancia de dois pontos
def distance_between(p1,p2):

    distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )

    return distance

#Esta funcao recolhe a cor e a forma que o utlizador deseja detetar na imagem que inseriu no programa
def user_input():
    
    cor = input("Que cor deseja detetar? ")   
    forma = input("Que forma deseja detetar? ")   
    return cor, forma

#Esta funcao escolhe um intervalo um HSV color range da cor que o utilizador escolheu 
#para ir procurar na imagem uma forma com essa cor
def escolher_cor(color):
    
    if color == "Vermelho" or color == "vermelho" or color == "red":
        lower = np.array([0,0,100],dtype=np.uint8)
        upper = np.array([10,100,255],dtype=np.uint8) 

        
    elif color == "Preto" or color == "preto" or color == "black":
        lower = np.array([0,0,0], dtype=np.uint8)
        upper = np.array([170,150,50], dtype=np.uint8)
    
       
    elif color == "Amarelo" or color == "amarelo" or color == "yellow":
        lower = np.array([0, 100, 100],np.uint8)
        upper = np.array([40, 255, 255],dtype=np.uint8)
        
    
    elif color == "Verde" or color == "verde" or color == "green":
        lower = np.array([38, 100, 100],np.uint8)
        upper = np.array([75, 255, 255],dtype=np.uint8)
    
     
    elif color == "Laranja" or color == "laranja" or color == "orange":
        lower = np.array([10, 70, 50],np.uint8)
        upper = np.array([60, 255, 255],dtype=np.uint8)
        
    elif color == "Azul" or color == "azul" or color == "blue":
        lower = np.array([80, 50, 50],np.uint8)
        upper = np.array([230, 255, 255],dtype=np.uint8)
        
    elif color == "Roxo" or color == "roxo" or color == "purple":
        lower = np.array([125, 150, 100],np.uint8)
        upper = np.array([155, 255, 255],dtype=np.uint8)
    
    elif color == "todas" or color == "all":
        lower = True
    
    else:
        print("Essa cor nao esta definida")
        
        
    return lower, upper
       
#esta funcao recebe a imagem com varias formas e deteta aquelas com a cor e forma que o usuario quer
def detetor_formas():
    
    
    #Leitura da imagem com formas geometricas
    img = cv2.imread('formas5.png')
    cor, forma = user_input()

    lower, upper = escolher_cor(cor)

    #imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    mask = cv2.inRange(img, lower, upper)
    kernel = np.ones((2, 2), np.uint8)
    mask = cv2.erode(mask, kernel)
    cv2.imshow("2", mask)
    
    
    #Caso a imagem tenha pixels com cor abaixo de 200 entao o valor dos pixels passa para 0,se
    #a cor for maior que 200, esses pixels passam para o valor máximo,que em geral é 255
    _, thrash = cv2.threshold(mask,200,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)

    #Lista dos diferentes contornos encontrados na imagem
    contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    #vai se percorrer o contorno de cada poligno individualmente
    lista_formas = ['Triangulo','triangulo','Quadrado','quadrado','Retangulo','retangulo','Pentagono','pentagono','Hexagono','hexagono'
                    'Estrela','estrela','Circulo','circulo','Elipse','elipse']
    lista1 = [3,4,5,6,10]
    if forma not in lista_formas:
        print('O programa nao consegue detetar essa forma')
    for contour in contours:
        #O epsilon representa a distância máxima entre a aproximação de um 
        #contorno de forma do polígono de entrada e do polígono de entrada original
        epsilon =  0.01* cv2.arcLength(contour, True)
        
        approx = cv2.approxPolyDP(contour,epsilon, True)
        
        #desenha-se os contornos de cada poligno na imagem
        #cv2.drawContours(img, [approx], 0, (0, 0, 0), 2)
        
        #coordenadas para colocar o texto do nome da detecao obtida
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5
        
        #Caso do triangulo
        if len(approx) == 3 and (forma == "triangulo" or forma == "Triangulo"):
            cv2.drawContours(img, [approx], 0, (0, 0, 0), 2) #desenha-se os contornos de cada triangulo na imagem
            cv2.putText(img, "Triangulo", (x, y), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0))
        #Caso dos quadrilateros   
        elif len(approx) == 4 :
            x1 ,y1, w, h = cv2.boundingRect(approx)
            #calcular a relacao entre os lados maiores e os mais pequenos
            aspectRatio = float(w)/h
            
            if aspectRatio >= 0.85 and aspectRatio <= 1.15 and (forma == "quadrado" or forma == "Quadrado"):
                cv2.drawContours(img, [approx], 0, (0, 0, 0), 2)
                cv2.putText(img, "Quadrado", (x, y), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0))
            elif aspectRatio >= 0.85 and aspectRatio <= 1.15 and (forma == "retangulo" or forma == "Retangulo"):
                cv2.drawContours(img, [approx], 0, (0, 0, 0), 2) 
                cv2.putText(img, "Retangulo", (x, y), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0))
        #Caso do pentagono
        elif len(approx) == 5 and (forma == "pentagono" or forma == "Pentagono"):
            cv2.drawContours(img, [approx], 0, (0, 0, 0), 2)
            cv2.putText(img, "Pentagono", (x-45, y-35), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0))
        #Caso do Hexagono
        elif len(approx) == 6 and (forma == "hexagono" or forma == "Hexagono"):
            cv2.drawContours(img, [approx], 0, (0, 0, 0), 2)
            cv2.putText(img, "Hexagono", (x, y), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0))
        #Caso da Estrela
        elif len(approx) == 10 and (forma == "estrela" or forma == "Estrela"):
            cv2.drawContours(img, [approx], 0, (0, 0, 0), 2)
            cv2.putText(img, "Estrela", (x-30, y+4), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0))
            
        #elif len(approx) in lista1:
        #    pass
        else:
            #Calcular os pontos mais à esquerda e mais à direita 
            leftmost = tuple(approx[approx[:,:,0].argmin()][0])
            rightmost = tuple(approx[approx[:,:,0].argmax()][0])
            topmost = tuple(approx[approx[:,:,1].argmin()][0])
            bottommost = tuple(approx[approx[:,:,1].argmax()][0])

            #print(distance_between(leftmost,rightmost))
            #print(distance_between(topmost,bottommost))
            #Condicoes para o caso em que é uma elipse e para quando é um circulo
            
            if abs(distance_between(leftmost,rightmost) - distance_between(topmost,bottommost)) < 15 and (forma == "circulo" or forma == "Circulo"):
                cv2.drawContours(img, [approx], 0, (0, 0, 0), 2)
                cv2.putText(img, "Circulo", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
            elif abs(distance_between(leftmost,rightmost) - distance_between(topmost,bottommost)) > 15 and (forma == "elipse" or forma == "elipse") : 
                cv2.drawContours(img, [approx], 0, (0, 0, 0), 2)
                cv2.putText(img, "Elipse", (x-55, y-20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
            
  


    cv2.imshow("Formas Geometricas", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

detetor_formas()
