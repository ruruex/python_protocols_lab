import pickle

# 示例1：基本数据类型的序列化与反序列化（使用文件）
def basic_example():
    # 定义一个对象（字典）
    data = {
        "name": "Alice",
        "age": 30,
        "hobbies": ["reading", "coding"]
    }
    
    # 序列化到文件
    with open("data.pkl", "wb") as f:  # 注意用二进制模式"wb"
        pickle.dump(data, f)
    print("示例1：数据已序列化到 data.pkl")
    
    # 从文件反序列化
    with open("data.pkl", "rb") as f:  # 二进制模式"rb"读取
        loaded_data = pickle.load(f)
    print("示例1：反序列化后的数据：", loaded_data)
    print("类型是否一致：", type(loaded_data) == type(data))  # True


# 示例2：内存中的序列化与反序列化（不使用文件）
def in_memory_example():
    # 定义一个列表对象
    my_list = [1, 2, 3, ("a", "b"), {"key": "value"}]
    
    # 序列化到字节流（内存中）
    byte_data = pickle.dumps(my_list)
    print(type(byte_data))
    print("\n示例2：序列化后的字节流：", byte_data)  # 字节类型数据
    
    # 从字节流反序列化
    restored_list = pickle.loads(byte_data)
    print("示例2：反序列化后的列表：", restored_list)
    print("内容是否一致：", restored_list == my_list)  # True
    
if __name__ == "__main__":
    basic_example()
    in_memory_example()