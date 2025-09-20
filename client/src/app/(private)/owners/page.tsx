"use client"

import DashLayout from "@/components/layout/DashLayout"
import { useToast } from "@/components/toast/ToastProvider"
import { PlayfairDisplay } from "@/components/ui/Fonts/Font"
import Input from "@/components/ui/Input"
import Modal from "@/components/ui/Modal"; // ✅ import reusable modal
import { addPetOwner, getPetOwners } from "@/lib/api/owners"
import { UserRoundPlus } from "lucide-react";
import { useRouter } from 'next/navigation';
import React, { FormEvent, useEffect, useState } from "react"

type Owner = {
  id: string
  name: string
  email: string
  phone_number: string
  address: string
}

const Page: React.FC = () => {
  const router = useRouter();
  const { showSuccess, showError } = useToast();
  const [owners, setOwners] = useState<Owner[]>([]);
  const [showAddModal, setShowAddModal] = useState(false)
  const [form, setForm] = useState<Omit<Owner, "id">>({
    name: "",
    email: "",
    phone_number: "",
    address: "",
  })

  const openAdd = () => {
    setForm({ name: "", email: "", phone_number: "", address: "" })
    setShowAddModal(true)
  }

  const closeAdd = () => setShowAddModal(false)

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    try {
      if (!form.name.trim() || !form.email.trim()) return

      const newOwner: Owner = {
        id: Date.now().toString(),
        ...form,
      }
      const response = await addPetOwner(form);
      if (response?.id) {
        setOwners((prev) => [newOwner, ...prev])
        showSuccess('Added Successfully!', `${response.name} pet owner added`, 5000);
      }
      closeAdd();
    } catch (error) {
      showError('Not added', `Try again !`, 5000);
    }
  }

  const handleOwnerClick = (id: string) => {
    router.push(`/owners/${id}`);
  }

  const getInitials = (name: string) => {
    const names = name.split(" ")
    if (names.length > 1) {
      return `${names[0][0]}${names[names.length - 1][0]}`.toUpperCase()
    }
    return name.substring(0, 2).toUpperCase()
  }

  useEffect(() => {
    const fetchOwners = async () => {
      try {
        const data = await getPetOwners({ skip: 0, limit: 10 });
        setOwners(data?.owners || data?.pets || []);
      } catch (error) {
        console.error("Failed to fetch owners:", error);
      }
    };

    fetchOwners();
  }, []);


  return (
    <DashLayout>
      <div className="p-8 min-h-screen text-text-primary">
        {/* Header */}
        <header className="flex items-center justify-between pb-6 mb-8 border-b border-border-primary">
          <h1 className="text-3xl font-bold tracking-tight">Pet Owners</h1>
          <button
            onClick={openAdd}
            className={`${PlayfairDisplay.className} gap-2 inline-flex items-center px-4 py-2 bg-secondary/90 text-white rounded-md shadow-md hover:brightness-95 transition-all duration-300 cursor-pointer`}
          >
            <UserRoundPlus size={16} />
            Add Owner
          </button>
        </header>

        {/* Owners list */}
        {owners.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-64 rounded-lg bg-background-secondary border border-dashed border-border-secondary">
            <p className="text-center text-text-muted">
              No owners yet. Click "Add Owner" to create one.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {owners.map((owner) => (
              <div
                key={owner.id}
                className="bg-background-secondary rounded-lg shadow-md border border-border-primary p-5 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 cursor-pointer"
                onClick={() => handleOwnerClick(owner.id)}
              >
                <div className="flex items-center">
                  <div className="w-12 h-12 rounded-full bg-primary-pastel text-primary flex items-center justify-center font-bold text-xl mr-4 flex-shrink-0">
                    {getInitials(owner.name)}
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-text-primary truncate">
                      {owner.name}
                    </h3>
                    <p className="text-sm text-text-secondary truncate">
                      {owner.email}
                    </p>
                  </div>
                </div>

                <div className="mt-4 pt-4 border-t border-border-primary space-y-3 text-sm">
                  <div className="flex items-start">
                    <span className="w-5 h-5 text-text-secondary mr-3 mt-0.5 flex-shrink-0">
                      📞
                    </span>
                    <span className="text-text-primary">{owner.phone_number}</span>
                  </div>
                  <div className="flex items-start">
                    <span className="w-5 h-5 text-text-secondary mr-3 mt-0.5 flex-shrink-0">
                      📍
                    </span>
                    <span className="text-text-primary">{owner.address}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Add Owner Modal */}
        {showAddModal && (
          <Modal title="Add New Pet Owner" onClose={closeAdd}>
            <form onSubmit={handleSubmit} className="space-y-4">
              <Input
                label="Full Name"
                buttonType="text"
                name="name"
                value={form.name}
                onChange={handleChange}
                required
              />
              <Input
                label="Email Address"
                buttonType="email"
                name="email"
                value={form.email}
                onChange={handleChange}
                required
              />
              <Input
                label="Phone Number"
                buttonType="tel"
                name="phone_number"
                value={form.phone_number}
                onChange={handleChange}
              />
              <Input
                label="Address"
                buttonType="text"
                name="address"
                value={form.address}
                onChange={handleChange}
              />
              <div className={`flex justify-end gap-3 pt-4 ${PlayfairDisplay.className}`}>
                <button
                  type="button"
                  onClick={closeAdd}
                  className="px-4 py-2 rounded-md border border-border-secondary text-text-secondary font-semibold hover:bg-background-muted transition-colors cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 bg-secondary/95 text-white font-semibold rounded-md shadow-sm hover:brightness-95 transition-colors cursor-pointer"
                >
                  Create Owner
                </button>
              </div>
            </form>
          </Modal>
        )}
      </div>
    </DashLayout>
  )
}

export default Page
