import math
import random
import time
import noise

import chunk

import block_type
import texture_manager

class World:
	def __init__(self):
		self.texture_manager = texture_manager.Texture_manager(16, 16, 256)
		self.blocks = [None]
		
		file = open('blocks.txt', 'r')
		lines = file.readlines()
		file.close()

		for line in lines: 
			exec(line.strip())

		self.texture_manager.generate_mipmaps()
		self.chunks = {}

		seedx = random.randint(-10000, 10000)
		seedy = random.randint(-10000, 10000)
		seedz = random.randint(-10000, 10000)

		print(f"Seed: {seedx}.{seedy}.{seedz}")

		for x in range(8):
			for z in range(8):
				for y in range(8):
					chunk_position = (x - 4, y - 4, z - 4)
					current_chunk = chunk.Chunk(self, chunk_position)

					for i in range(chunk.CHUNK_WIDTH):
						for j in range(chunk.CHUNK_HEIGHT):
							for k in range(chunk.CHUNK_LENGTH):
								if noise.pnoise3((float(i + x * chunk.CHUNK_WIDTH) / 16) + seedx, (float(j + y * chunk.CHUNK_HEIGHT) / 16) + seedy, (float(k + z * chunk.CHUNK_LENGTH) / 16) + seedz) > 0.0:
									if not noise.pnoise3((float(i + x * chunk.CHUNK_WIDTH) / 16) + seedx, (float(j + y * chunk.CHUNK_HEIGHT) / 16) + seedy + (1 / 16), (float(k + z * chunk.CHUNK_LENGTH) / 16) + seedz) > 0.0:
										current_chunk.blocks[i * chunk.CHUNK_LENGTH * chunk.CHUNK_HEIGHT + j * chunk.CHUNK_LENGTH + k] = 3
									else:
										for w in range(2, 6):
											if not noise.pnoise3((float(i + x * chunk.CHUNK_WIDTH) / 16) + seedx, (float(j + y * chunk.CHUNK_HEIGHT) / 16) + seedy + (w / 16), (float(k + z * chunk.CHUNK_LENGTH) / 16) + seedz) > 0.0:
												current_chunk.blocks[i * chunk.CHUNK_LENGTH * chunk.CHUNK_HEIGHT + j * chunk.CHUNK_LENGTH + k] = 4
											else:
												current_chunk.blocks[i * chunk.CHUNK_LENGTH * chunk.CHUNK_HEIGHT + j * chunk.CHUNK_LENGTH + k] = 5
								else:
									current_chunk.blocks[i * chunk.CHUNK_LENGTH * chunk.CHUNK_HEIGHT + j * chunk.CHUNK_LENGTH + k] = 0

					self.chunks[chunk_position] = current_chunk

		for chunk_position in self.chunks:
			self.chunks[chunk_position].update_mesh()

	def get_block(self, position):
		x, y, z = position

		chunk_x = math.floor(x / chunk.CHUNK_WIDTH)
		chunk_y = math.floor(y / chunk.CHUNK_HEIGHT)
		chunk_z = math.floor(z / chunk.CHUNK_LENGTH)

		local_x = int(x % chunk.CHUNK_WIDTH)
		local_y = int(y % chunk.CHUNK_HEIGHT)
		local_z = int(z % chunk.CHUNK_LENGTH)

		chunk_position = (chunk_x, chunk_y, chunk_z)

		if not chunk_position in self.chunks:
			return self.blocks[0]
		
		return self.blocks[self.chunks[chunk_position].blocks[local_x * chunk.CHUNK_LENGTH * chunk.CHUNK_HEIGHT + local_y * chunk.CHUNK_LENGTH + local_z]]

	def draw(self, position):
		for chunk_position in self.chunks:
			x = int(position[0] / chunk.CHUNK_WIDTH  - chunk_position[0])
			y = int(position[1] / chunk.CHUNK_HEIGHT - chunk_position[1])
			z = int(-position[2] / chunk.CHUNK_LENGTH - chunk_position[2])

			if math.sqrt(x * x + y * y + z * z) < 4:
				self.chunks[chunk_position].draw()
