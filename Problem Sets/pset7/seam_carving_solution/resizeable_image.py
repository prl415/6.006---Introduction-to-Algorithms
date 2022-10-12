import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self):
        #Each cell consists of 3 elements: (pixel energy, loc of current pixel, loc of parent pixel)
        path_cost_matrix = [[(self.energy(j, i), (i, j), (i, j)) for j in range(self.width)] for i in range(self.height)]
        
        for i in range(1, self.height):
            for j in range(self.width):
                
                #Special case 1: At the left edge
                if j == 0:
                    result = min([path_cost_matrix[i - 1][j], path_cost_matrix[i - 1][j + 1]], key = lambda x: x[0])
                    
                #Special case 2: At the right edge
                if j == (self.width - 1):
                    result = min([path_cost_matrix[i - 1][j - 1], path_cost_matrix[i - 1][j]], key = lambda x: x[0])
                
                else:
                    result = min([path_cost_matrix[i - 1][j - 1], path_cost_matrix[i - 1][j], path_cost_matrix[i - 1][j + 1]], key = lambda x: x[0])
        
                
                path_cost_matrix[i][j] = (result[0] + path_cost_matrix[i][j][0], path_cost_matrix[i][j][1], result[1])
                
        height_index = self.height - 1
        path = list(min(path_cost_matrix[height_index], key = lambda x: x[0])[1:])
        
        while height_index > 1:
            height_index -= 1
            row, col = path[-1]
            path.append(path_cost_matrix[row][col][2])
        
        path.reverse()
        
        path = [(loc[1], loc[0]) for loc in path]
        
        return path
        
    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
